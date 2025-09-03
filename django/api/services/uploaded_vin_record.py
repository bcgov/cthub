import pandas as pd
from django.utils import timezone
from api.models.uploaded_vin_record import UploadedVinRecord
from api.constants.decoder import get_service


def parse_and_save(uploaded_vins_file, file_response):
    chunks = pd.read_csv(file_response, sep="|", chunksize=uploaded_vins_file.chunksize)
    start_index = uploaded_vins_file.start_index
    end_index = start_index + uploaded_vins_file.chunks_per_iteration
    processed = True
    for idx, df in enumerate(chunks):
        if idx < start_index:
            continue
        elif idx >= start_index and idx < end_index:
            df.fillna("", inplace=True)
            vins = []
            for _, row in df.iterrows():
                if row["vin"] != "":
                    vins.append(row["vin"])
            df_records_map = get_df_records_map(df)
            existing_records_map = get_existing_records_map(vins)
            records_to_insert = get_records_to_insert(
                df_records_map, existing_records_map
            )
            UploadedVinRecord.objects.bulk_create(records_to_insert)
            records_to_update = get_records_to_update(
                df_records_map, existing_records_map
            )
            UploadedVinRecord.objects.bulk_update(
                records_to_update, ["data", "change", "update_timestamp"]
            )
        else:
            processed = False
            break
    if processed:
        UploadedVinRecord.objects.exclude(
            update_timestamp__gte=uploaded_vins_file.create_timestamp
        ).update(
            change=UploadedVinRecord.Change.REMOVED, update_timestamp=timezone.now()
        )
    uploaded_vins_file.processed = processed
    uploaded_vins_file.start_index = end_index
    uploaded_vins_file.save()


# returns a dict of vin -> data
def get_df_records_map(df):
    result = {}
    for _, row in df.iterrows():
        vin = row["vin"]
        if vin:
            data = row.to_dict()
            del data["vin"]
            result[vin] = data
    return result


# returns a dict of vin -> id
def get_existing_records_map(vins):
    result = {}
    records = UploadedVinRecord.objects.only("id", "vin").filter(vin__in=vins)
    for record in records:
        result[record.vin] = record.id
    return result


# df_records_map should be dict of vin -> data
# existing_records_map should be dict of vin -> id
def get_records_to_insert(df_records_map, existing_records_map):
    result = []
    for vin, data in df_records_map.items():
        if vin not in existing_records_map:
            result.append(
                UploadedVinRecord(
                    vin=vin,
                    data=data,
                )
            )
    return result


# df_records_map should be dict of vin -> data
# existing_records_map should be dict of vin -> id
# assumes that there are no duplicate vins in the same file
def get_records_to_update(df_records_map, existing_records_map):
    result = []
    for vin, data in df_records_map.items():
        if vin in existing_records_map:
            existing_record_id = existing_records_map[vin]
            result.append(
                UploadedVinRecord(
                    id=existing_record_id,
                    data=data,
                    update_timestamp=timezone.now(),
                    change=UploadedVinRecord.Change.MODIFIED,
                )
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
