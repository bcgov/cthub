from django.conf import settings
from api.services.minio import get_minio_client, get_minio_object
from func_timeout import func_timeout, FunctionTimedOut
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.decoder_constants import get_service
from api.utilities.generic import get_map
from api.services.decoded_vin_record import save_decoded_data
from api.services.uploaded_vin_record import parse_and_save
from django.db import transaction


def create_minio_bucket():
    bucket_name = settings.MINIO_BUCKET_NAME
    client = get_minio_client()
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)


def read_uploaded_vins_file():
    # TODO: this job will probably have to become more involved; it currently just uploads whatever is in the file while skipping records
    # that encounter uniqueness conflicts.
    # we'll probably have to do an initial, chunked read from the
    # file in order to build a map of (vin, postal_code) -> (record chunk index, record index within chunk) of unique records (based on snapshot_date?),
    # then we'll have to compare the (vin, postal_code) keys to existing records in the database, and
    # determine which ones need to get bulk-inserted, and which ones bulk-updated.
    # also have to keep in mind the memory used by any data structures we use
    def close_file_response(file_response):
        if file_response is not None:
            file_response.close()
            file_response.release_conn()

    @transaction.atomic
    def inner(vins_file, file_response):
        if vins_file is not None and file_response is not None:
            parse_and_save(vins_file, file_response)

    file_response = None
    vins_file = (
        UploadedVinsFile.objects.filter(processed=False)
        .order_by("create_timestamp")
        .first()
    )
    if vins_file is not None:
        file_response = get_minio_object(vins_file.filename)
    try:
        func_timeout(600, inner, args=(vins_file, file_response))
        close_file_response(file_response)
    except FunctionTimedOut:
        print("reading vins file job timed out")
        close_file_response(file_response)
        raise Exception
    except Exception:
        close_file_response(file_response)
        raise Exception


def batch_decode_vins(service_name, batch_size=50):
    def inner():
        max_decode_attempts = settings.MAX_DECODE_ATTEMPTS
        service = get_service(service_name)
        if service:
            decoded_vin_model = service.MODEL.value
            filters = {
                service.CURRENT_DECODE_SUCCESSFUL.value: False,
                service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value
                + "__lt": max_decode_attempts,
            }
            order_by = [
                service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value,
                "create_timestamp",
            ]
            uploaded_vin_records = UploadedVinRecord.objects.filter(**filters).order_by(
                *order_by
            )[:batch_size]
            uploaded_vins = set()
            for uploaded_record in uploaded_vin_records:
                uploaded_vins.add(uploaded_record.vin)
            vins_to_update = set()
            decoded_records_to_update_map = get_map(
                "vin", decoded_vin_model.objects.filter(vin__in=uploaded_vins)
            )
            for decoded_vin in decoded_records_to_update_map:
                vins_to_update.add(decoded_vin)
            vins_to_insert = uploaded_vins.difference(vins_to_update)

            decoder = service.BATCH_DECODER.value
            decoded_data = decoder(uploaded_vin_records)

            save_decoded_data(
                uploaded_vin_records,
                vins_to_insert,
                decoded_records_to_update_map,
                service_name,
                decoded_data,
            )

    try:
        func_timeout(45, inner)
    except FunctionTimedOut:
        print("batch decode vins job timed out")
        raise Exception
