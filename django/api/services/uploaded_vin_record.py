import traceback
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.services.icbc import get_header
from api.utilities.icbc import get_record
from api.constants.decoder import get_service, ICBC_FILE


def parse_and_save(uploaded_vins_file, file_response):
    statuses = UploadedVinsFile.FileStatus
    status = uploaded_vins_file.status
    headers = uploaded_vins_file.headers
    bytes_read = 0
    new_status = None

    try:
        if status == statuses.NEW:
            headers_result = get_header(file_response)
            headers = headers_result[0]
            bytes_read = bytes_read + headers_result[1]
            new_status = statuses.PROCESSING
        elif status == statuses.PROCESSING:
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_vins(file_response, headers)
                bytes_read = bytes_read + result[0]
                end_of_file = result[1]
                if end_of_file:
                    break
            if end_of_file:
                new_status = statuses.SUCCESS
            else:
                new_status = statuses.PROCESSING
    except:
        traceback.print_exc()
        uploaded_vins_file.status = UploadedVinsFile.FileStatus.ERROR
        uploaded_vins_file.save(using="other")
        raise Exception()

    if status == statuses.NEW:
        uploaded_vins_file.headers = headers
    uploaded_vins_file.status = new_status
    uploaded_vins_file.byte_offset = uploaded_vins_file.byte_offset + bytes_read
    uploaded_vins_file.save()


def save_vins(file_response, headers):
    bytes_read = 0
    uploaded_vin_records_to_create = []
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        bytes_read = bytes_read + record[1]
        vin = record[0]
        uploaded_vin_records_to_create.append(UploadedVinRecord(vin=vin))
    if uploaded_vin_records_to_create:
        UploadedVinRecord.objects.bulk_create(
            uploaded_vin_records_to_create, ignore_conflicts=True
        )
    return (bytes_read, end_of_file)


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
