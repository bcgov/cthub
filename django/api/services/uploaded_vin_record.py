import traceback
import pandas as pd
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.models.icbc import IcbcRecord
from api.constants.decoder import get_service, ICBC_FILE


def parse_and_save(uploaded_vins_file, file_response):
    """Parse uploaded VIN files. For ICBC files apply full preprocessing and track changes"""

    is_icbc = uploaded_vins_file.icbc
    start_index = uploaded_vins_file.start_index
    end_index = start_index + uploaded_vins_file.chunks_per_iteration
    status_to_save = UploadedVinsFile.FileStatus.SUCCESS

    try:
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
                if is_icbc:
                    df = preprocess_chunk(df)
                    df.fillna("", inplace=True)
                    icbc_records_to_create = get_icbc_records_to_create(df)
                    IcbcRecord.objects.bulk_create(icbc_records_to_create)
                uploaded_vin_records_to_create = get_uploaded_vin_records_to_create(df)
                UploadedVinRecord.objects.bulk_create(
                    uploaded_vin_records_to_create, ignore_conflicts=True
                )
            else:
                status_to_save = UploadedVinsFile.FileStatus.PROCESSING
                break
    except:
        status_to_save = UploadedVinsFile.FileStatus.ERROR
        end_index = start_index
        traceback.print_exc()

    uploaded_vins_file.status = status_to_save
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
    return df


def get_icbc_records_to_create(df):
    result = []
    for _, row in df.iterrows():
        result.append(
            IcbcRecord(
                vin=row.get("vin"),
                electric_vehicle_flag=row.get("electric_vehicle_flag"),
                fuel_type=row.get("fuel_type"),
                hybrid_vehicle_flag=row.get("hybrid_vehicle_flag"),
                make=row.get("make"),
                model=row.get("model"),
                model_year=row.get("model_year"),
                vehicle_registration_date=row.get("vehicle_registration_date"),
                snapshot_date=row.get("snapshot_date"),
                # todo: the other fields
            )
        )
    # todo: track changes
    return result


def get_uploaded_vin_records_to_create(df):
    result = []
    for _, row in df.iterrows():
        vin = row.get("vin")
        if vin:
            transformed_vin = str(vin).strip().upper()
            if transformed_vin:
                result.append(
                    UploadedVinRecord(
                        vin=transformed_vin,
                    )
                )
    return result


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
