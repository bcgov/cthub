import traceback
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.utilities.icbc import get_record
from api.services.icbc import write_to_disk
from api.constants.decoder import get_service, ICBC_FILE
from django.utils import timezone


def parse_and_save(uploaded_vins_file, file_response):
    statuses = UploadedVinsFile.FileStatus
    status = uploaded_vins_file.status
    headers = uploaded_vins_file.headers

    try:
        if status == statuses.NEW:
            write_to_disk(file_response, uploaded_vins_file.filename)
            uploaded_vins_file.status = statuses.SUCCESS_WRITING_FILE_TO_DISK
        else:
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                end_of_file = save_vins(file_response, headers)
                if end_of_file:
                    break
            uploaded_vins_file.byte_offset = file_response.tell()
            if end_of_file:
                uploaded_vins_file.status = statuses.SUCCESS
            else:
                uploaded_vins_file.status = statuses.PROCESSING
    except:
        traceback.print_exc()
        UploadedVinsFile.objects.filter(id=uploaded_vins_file.id).using("other").update(
            status=statuses.ERROR, update_timestamp=timezone.now()
        )
        raise Exception()

    uploaded_vins_file.save()


def save_vins(file_response, headers):
    uploaded_vin_records_to_create = []
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        vin = record[0]
        if vin:
            uploaded_vin_records_to_create.append(UploadedVinRecord(vin=vin))
    if uploaded_vin_records_to_create:
        UploadedVinRecord.objects.bulk_create(
            uploaded_vin_records_to_create, ignore_conflicts=True
        )
    return end_of_file


def get_decode_successful(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.DECODE_SUCCESSFUL.value)


def set_decode_successful(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.DECODE_SUCCESSFUL.value, value)


def get_number_of_decode_attempts(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.NUMBER_OF_DECODE_ATTEMPTS.value)


def set_number_of_decode_attempts(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.NUMBER_OF_DECODE_ATTEMPTS.value, value)
