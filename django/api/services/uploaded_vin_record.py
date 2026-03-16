import pandas as pd
from django.utils import timezone
from api.models.uploaded_vin_record import UploadedVinRecord
from api.constants.decoder import get_service, ICBC_FILE


def parse_and_save(uploaded_vins_file, file_response):
    """Parse uploaded VIN files. For ICBC files apply full preprocessing; otherwise treat as plain VIN list."""

    is_icbc = getattr(uploaded_vins_file, "icbc", True)

    start_index = uploaded_vins_file.start_index
    end_index = start_index + uploaded_vins_file.chunks_per_iteration
    processed = True

    if is_icbc:
        chunks = pd.read_csv(
            file_response,
            chunksize=uploaded_vins_file.chunksize,
            sep=ICBC_FILE.DELIMITER.value,
            na_values=ICBC_FILE.NA_VALUES.value,
            dtype=ICBC_FILE.DATA_TYPES.value,
        )

        for idx, df in enumerate(chunks):
            if idx < start_index:
                continue
            elif idx >= start_index and idx < end_index:
                preprocess_chunk(df)
                df.fillna("", inplace=True)
                vins = []
                for _, row in df.iterrows():
                    vin = row["vin"]
                    if len(vin) == 17:
                        vins.append(vin)
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
                change=UploadedVinRecord.Change.REMOVED,
                update_timestamp=timezone.now(),
            )
    else:
        print('test')
        chunks = pd.read_csv(
            file_response,
            chunksize=uploaded_vins_file.chunksize,
            header=None,
            names=["vin"],
        )

        for idx, df in enumerate(chunks):
            print(df)
            if idx < start_index:
                continue
            if idx >= end_index:
                processed = False
                break

            vins = (
                df["vin"]
                .astype(str)
                .str.strip()
                .str.upper()
            )
            vins = [vin for vin in vins if len(vin) == 17]

            if len(vins) == 0:
                continue

            existing_records_map = get_existing_records_map(vins)
            records_to_insert = []
            records_to_update = []
            now = timezone.now()

            for vin in vins:
                if vin in existing_records_map:
                    records_to_update.append(
                        UploadedVinRecord(
                            id=existing_records_map[vin],
                            update_timestamp=now,
                            change=UploadedVinRecord.Change.MODIFIED,
                        )
                    )
                else:
                    print(vin)
                    records_to_insert.append(UploadedVinRecord(vin=vin, data={}))

            if records_to_insert:
                UploadedVinRecord.objects.bulk_create(records_to_insert)
            if records_to_update:
                UploadedVinRecord.objects.bulk_update(
                    records_to_update, ["update_timestamp", "change"]
                )

    uploaded_vins_file.processed = processed
    uploaded_vins_file.start_index = end_index
    uploaded_vins_file.save()


def format_case(s, case="skip"):
    if len(s.dropna()) != 0:
        output = (
            s[
                s.notna()
            ]  # I am applying this function to non NaN values only. If you do not, they get converted from NaN to nan and are more annoying to work with.
            .astype(str)  # Convert to string
            .str.strip()  # Strip white spaces (this dataset suffers from extra tabs, lines, etc.)
        )
        if case == "title":
            return output.str.title()
        elif case == "upper":
            return output.str.upper()
        elif case == "lower":
            return output.str.lower()
        elif case == "skip":
            pass


def format_numbers(s):
    if len(s.dropna()) != 0:
        output = pd.to_numeric(
            s[
                s.notna()
            ]  # I am applying this function to non NaN values only. If you do not, they get converted from NaN to nan and are more annoying to work with.
            .astype(str)  # Convert to string
            .str.strip()
            .str.replace(
                ",", ""
            )  # Strip white spaces (this dataset suffers from extra tabs, lines, etc.)
            .str.replace(" ", "")
        )
        return output


def preprocess_chunk(df):
    df.columns = df.columns.str.lower()
    df.drop(columns=ICBC_FILE.COLUMNS_TO_DROP.value, inplace=True)
    numeric_cols = list(
        set(ICBC_FILE.NUMERIC_COLUMNS.value).intersection(set(df.columns))
    )
    numeric_cols_w_strings = df[numeric_cols].select_dtypes("object").columns
    for col in numeric_cols_w_strings:
        df[col] = format_numbers(df[col])
    date_cols = list(set(ICBC_FILE.DATE_COLUMNS.value).intersection(set(df.columns)))
    for col in date_cols:
        s = (pd.to_datetime(df[col], yearfirst=True, utc=True).dt.date).astype(str)
        df[col] = s.where(s != "NaT")
    for key, cols in ICBC_FILE.MODIFICATION_MAP.value.items():
        col_subset = list(set(cols).intersection(df.columns))
        if len(col_subset) != 0:
            for col in col_subset:
                df[col] = format_case(df[col], case=key)


# returns a dict of vin -> data
def get_df_records_map(df):
    result = {}
    for _, row in df.iterrows():
        vin = row["vin"]
        if len(vin) == 17:
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
