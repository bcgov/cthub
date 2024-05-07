import pandas as pd
from api.models.uploaded_vin_record import UploadedVinRecord
from api.decoder_constants import get_service


def parse_and_save(uploaded_vins_file, file_response):
    processed = True
    number_of_chunks_processed = 0
    number_of_chunks_to_process = uploaded_vins_file.chunks_per_run
    chunksize = uploaded_vins_file.chunk_size
    start_index = uploaded_vins_file.start_index
    chunks = pd.read_csv(file_response, sep="|", chunksize=chunksize)

    for idx, chunk in enumerate(chunks):
        if (
            idx >= start_index
            and number_of_chunks_processed < number_of_chunks_to_process
        ):
            vin_records_to_insert = get_vin_records_to_insert(chunk)
            UploadedVinRecord.objects.bulk_create(
                vin_records_to_insert,
                ignore_conflicts=True,
            )
            number_of_chunks_processed = number_of_chunks_processed + 1
        elif idx >= start_index + number_of_chunks_processed:
            processed = False
            break

    new_start_index = start_index + number_of_chunks_processed
    uploaded_vins_file.processed = processed
    uploaded_vins_file.start_index = new_start_index
    uploaded_vins_file.save()


def get_vin_records_to_insert(df):
    result = []
    df.fillna("", inplace=True)
    for _, row in df.iterrows():
        if row["vin"] != "":
            vin = row["vin"]
            postal_code = row["postal_code"]
            data = row.to_dict()
            del data["vin"]
            del data["postal_code"]
            result.append(
                UploadedVinRecord(vin=vin, postal_code=postal_code, data=data)
            )
    return result


def get_decode_successful(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.CURRENT_DECODE_SUCCESSFUL.value)


def set_decode_successful(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.CURRENT_DECODE_SUCCESSFUL.value, value)


def get_number_of_decode_attempts(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value)


def set_number_of_decode_attempts(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value, value)
