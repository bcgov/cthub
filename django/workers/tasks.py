from django.conf import settings
from api.services.minio import get_minio_client, get_minio_object
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.constants.decoder import get_service
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
    vins_file = (
        UploadedVinsFile.objects.filter(status=UploadedVinsFile.FileStatus.PROCESSING)
        .order_by("create_timestamp")
        .first()
    )
    if vins_file is not None:
        file_response = get_minio_object(vins_file.filename)
        if file_response is not None:
            with transaction.atomic():
                parse_and_save(vins_file, file_response)
            file_response.close()
            file_response.release_conn()


def batch_decode_vins(service_name, batch_size=50):
    max_decode_attempts = settings.MAX_DECODE_ATTEMPTS
    service = get_service(service_name)
    if service:
        filters = {
            service.DECODE_SUCCESSFUL.value: False,
            service.NUMBER_OF_DECODE_ATTEMPTS.value + "__lt": max_decode_attempts,
        }
        order_by = [
            service.NUMBER_OF_DECODE_ATTEMPTS.value,
            "create_timestamp",
        ]
        uploaded_vin_records = (
            UploadedVinRecord.objects.only("vin")
            .filter(**filters)
            .order_by(*order_by)[:batch_size]
        )
        decoder = service.BATCH_DECODER.value
        decoded_data = decoder(uploaded_vin_records)
        with transaction.atomic():
            save_decoded_data(
                uploaded_vin_records,
                service_name,
                decoded_data,
            )


def remove_cleaned_datasets():
    try:
        client = get_minio_client()
        objects = client.list_objects(
            settings.MINIO_BUCKET_NAME, prefix="cleaned_datasets/"
        )
        for obj in objects:
            client.remove_object(settings.MINIO_BUCKET_NAME, obj.object_name)
    except Exception:
        print("Error occurred when removing cleaned-datasets.")
