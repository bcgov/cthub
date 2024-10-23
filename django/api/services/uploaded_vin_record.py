from datetime import datetime
import pandas as pd
from django.utils import timezone
from api.models.uploaded_vin_record import UploadedVinRecord
from api.constants.decoder import get_service


def parse_and_save(uploaded_vins_file, file_response):
    processed = True
    start_index = uploaded_vins_file.start_index
    chunks = pd.read_csv(
        file_response, sep="|", chunksize=uploaded_vins_file.chunk_size
    )

    for idx, df in enumerate(chunks):
        if idx == start_index:
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
                records_to_update, ["data", "timestamp", "update_timestamp"]
            )
        elif idx > start_index:
            processed = False
            break

    uploaded_vins_file.processed = processed
    uploaded_vins_file.start_index = start_index + 1
    uploaded_vins_file.save()


# returns a dict of (vin, postal_code) -> {timestamp, data}
def get_df_records_map(df):
    result = {}
    for _, row in df.iterrows():
        vin = row["vin"]
        postal_code = row["postal_code"]
        df_timestamp = row["snapshot_date"]
        if vin and postal_code and df_timestamp:
            key = (vin, postal_code)
            timestamp = timezone.make_aware(
                datetime.strptime(df_timestamp, "%Y-%m-%d %H:%M:%S.%f")
            )
            df_data = row.to_dict()
            data = df_data if df_data else {}
            del data["vin"]
            del data["postal_code"]
            del data["snapshot_date"]
            if key in result:
                most_recent_ts = result[key]["timestamp"]
                if most_recent_ts < timestamp:
                    result[key] = {"timestamp": timestamp, "data": data}
            else:
                result[key] = {"timestamp": timestamp, "data": data}
    return result


# returns a dict of (vin, postal_code) -> {id, timestamp}
def get_existing_records_map(vins):
    result = {}
    records = UploadedVinRecord.objects.only(
        "id", "vin", "postal_code", "timestamp"
    ).filter(vin__in=vins)
    for record in records:
        key = (record.vin, record.postal_code)
        result[key] = {"id": record.id, "timestamp": record.timestamp}
    return result


# df_records_map should be dict of (vin, postal_code) -> {timestamp, data}
# existing_records_map should be dict of (vin, postal_code) -> {id, timestamp}
def get_records_to_insert(df_records_map, existing_records_map):
    result = []
    for key, value in df_records_map.items():
        if key not in existing_records_map:
            result.append(
                UploadedVinRecord(
                    vin=key[0],
                    postal_code=key[1],
                    timestamp=value["timestamp"],
                    data=value["data"],
                )
            )
    return result


# df_records_map should be dict of (vin, postal_code) -> {timestamp, data}
# existing_records_map should be dict of (vin, postal_code) -> {id, timestamp}
def get_records_to_update(df_records_map, existing_records_map):
    result = []
    for key, value in df_records_map.items():
        if key in existing_records_map:
            existing_record = existing_records_map[key]
            timestamp = value["timestamp"]
            if existing_record["timestamp"] < timestamp:
                result.append(
                    UploadedVinRecord(
                        id=existing_record["id"],
                        timestamp=timestamp,
                        data=value["data"],
                        update_timestamp=timezone.now(),
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
