import traceback
from datetime import datetime
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.models.icbc import IcbcRecord
from api.models.icbc_duplicate_vin import IcbcDuplicateVin
from api.models.icbc_vin_lookup import IcbcVinLookup
from api.services.uploaded_vins_file import get_prev_icbc_file
from api.utilities.icbc import (
    get_record,
    get_transformed_dict,
    get_untracked_and_tracked_records,
    get_created,
    get_modified,
    get_removed,
)
from api.constants.decoder import ICBC_FILE


def get_icbc_ev_records(vins):
    result = {}
    records = IcbcRecord.objects.filter(vin__in=vins).only(
        "vin",
        "electric_vehicle_flag",
        "fuel_type",
        "hybrid_vehicle_flag",
        "make",
        "model",
        "model_year",
        "vehicle_registration_date",
        "snapshot_date",
    )
    for record in records:
        ev_flag = record.electric_vehicle_flag
        hybrid_flag = record.hybrid_vehicle_flag
        fuel_type = record.fuel_type
        if (
            (ev_flag is not None and ev_flag.upper() == "Y")
            or (hybrid_flag is not None and hybrid_flag.upper() == "Y")
            or (fuel_type is not None and fuel_type.lower() == "electric")
            or (fuel_type is not None and fuel_type.lower() == "hydrogen")
            or (fuel_type is not None and fuel_type.lower() == "gasolineelectric")
        ):
            result[record.vin] = {
                "make": record.make,
                "model": record.model,
                "modelYear": record.model_year,
                "registrationDate": (
                    str(record.vehicle_registration_date)
                    if record.vehicle_registration_date
                    else None
                ),
                "snapshotDate": (
                    str(record.snapshot_date) if record.snapshot_date else None
                ),
            }
    return result


def icbc_parse_and_save(uploaded_vins_file, file_response):
    statuses = UploadedVinsFile.FileStatus
    status = uploaded_vins_file.status
    headers = uploaded_vins_file.headers
    first_snapshot_date = uploaded_vins_file.first_snapshot_date
    bytes_read = 0
    new_status = None

    try:
        if status == statuses.NEW:
            headers_result = get_header(file_response)
            headers = headers_result[0]
            bytes_read = bytes_read + headers_result[1]
            first_snapshot_date = save_duplicates_and_get_first_snapshot_date(
                file_response, headers
            )
            new_status = statuses.SUCCESS_SAVING_DUPLICATES
        elif (
            status == statuses.SUCCESS_SAVING_DUPLICATES
            or status == statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
        ):
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_created_and_modified(file_response, headers)
                bytes_read = bytes_read + result[0]
                end_of_file = result[1]
                if end_of_file:
                    break
            if end_of_file:
                prev_file = get_prev_icbc_file()
                if prev_file is None:
                    new_status = statuses.SUCCESS_TRACKING_REMOVED_RECORDS
                else:
                    new_status = statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS
            else:
                new_status = statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
        elif (
            status == statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS
            or status == statuses.TRACKING_REMOVED_RECORDS
        ):
            if status == statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS:
                headers_result = get_header(file_response)
                headers = headers_result[0]
                bytes_read = bytes_read + headers_result[1]
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_removed(file_response, headers, first_snapshot_date)
                bytes_read = bytes_read + result[0]
                end_of_file = result[1]
                if end_of_file:
                    break
            if end_of_file:
                new_status = statuses.SUCCESS_TRACKING_REMOVED_RECORDS
            else:
                new_status = statuses.TRACKING_REMOVED_RECORDS
        elif status == statuses.SUCCESS_TRACKING_REMOVED_RECORDS:
            delete_lookup_vins()
            new_status = statuses.SUCCESS
    except:
        traceback.print_exc()
        if status == statuses.NEW:
            error_status = statuses.ERROR_SAVING_DUPLICATES
        elif (
            status == statuses.SUCCESS_SAVING_DUPLICATES
            or status == statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
        ):
            error_status = statuses.ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS
        elif (
            status == statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS
            or status == statuses.TRACKING_REMOVED_RECORDS
        ):
            error_status = statuses.ERROR_TRACKING_REMOVED_RECORDS
        elif status == statuses.SUCCESS_TRACKING_REMOVED_RECORDS:
            error_status = statuses.ERROR_CLEARING_VIN_LOOKUP_TABLE
        uploaded_vins_file.status = error_status
        uploaded_vins_file.save(using="other")
        raise Exception()

    # set new status here, as well as new bytes_offset, and headers if it's a new file,
    # or if we're moving to the "track removals" stage
    if status == statuses.NEW:
        uploaded_vins_file.headers = headers
        uploaded_vins_file.first_snapshot_date = first_snapshot_date
    elif status == statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS:
        uploaded_vins_file.headers = headers
    uploaded_vins_file.status = new_status
    if new_status == statuses.SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS:
        uploaded_vins_file.byte_offset = 0
    else:
        uploaded_vins_file.byte_offset = uploaded_vins_file.byte_offset + bytes_read
    uploaded_vins_file.save()


# returns (list of headers, headers byte length)
def get_header(file_response):
    line = file_response.readline()
    headers = line.decode("utf-8")
    headers_list = [
        item.strip().lower() for item in headers.split(ICBC_FILE.DELIMITER.value)
    ]
    return (headers_list, len(line))


def save_duplicates_and_get_first_snapshot_date(file_response, headers):
    def save(duplicate_vins):
        duplicate_vin_records = []
        for dup_vin in duplicate_vins:
            duplicate_vin_records.append(IcbcDuplicateVin(vin=dup_vin))
        IcbcDuplicateVin.objects.bulk_create(
            duplicate_vin_records, ignore_conflicts=True
        )

    vin_index = headers.index("vin")
    snapshot_date_index = headers.index("snapshot_date")
    first_snapshot_date = None
    seen_vins = set()
    duplicate_vins = set()
    for line in file_response:
        decoded_line = line.decode("utf-8")
        record = [
            item.strip() for item in decoded_line.split(ICBC_FILE.DELIMITER.value)
        ]
        if first_snapshot_date is None:
            try:
                first_snapshot_date = datetime.strptime(
                    record[snapshot_date_index], ICBC_FILE.TS_FORMAT.value
                ).date()
            except:
                pass
        vin = record[vin_index].upper()
        if vin and vin not in ICBC_FILE.NA_VALUES.value and vin in seen_vins:
            duplicate_vins.add(vin)
        seen_vins.add(vin)
        if len(duplicate_vins) == 10000:
            save(duplicate_vins)
            duplicate_vins = set()
    if len(duplicate_vins) > 0:
        save(duplicate_vins)
    return first_snapshot_date


# returns (bytes read, eof reached)
def save_created_and_modified(file_response, headers):
    def save(vins_and_data):
        vins, _ = zip(*vins_and_data)
        duplicates = set(
            IcbcDuplicateVin.objects.filter(vin__in=vins).values_list("vin", flat=True)
        )
        untracked_df, tracked_records = get_untracked_and_tracked_records(
            vins_and_data, duplicates
        )
        icbc = (
            IcbcRecord.objects.filter(vin__in=tracked_records.keys())
            .order_by("vin", "-create_timestamp")
            .distinct("vin")
            .values()
        )
        icbc_records = {}
        for record in icbc:
            icbc_records[record["vin"]] = record
        created_df = get_created(icbc_records, tracked_records)
        modified_df = get_modified(icbc_records, tracked_records)
        icbc_records_to_create = []
        for df in [untracked_df, created_df, modified_df]:
            if df is not None:
                records = df.to_dict("records")
                for record in records:
                    transformed_dict = get_transformed_dict(record)
                    icbc_records_to_create.append(IcbcRecord(**transformed_dict))
        IcbcRecord.objects.bulk_create(icbc_records_to_create)
        uploaded_vin_records_to_create = []
        icbc_lookup_vins_to_create = []
        for vin in tracked_records.keys():
            uploaded_vin_records_to_create.append(UploadedVinRecord(vin=vin))
            icbc_lookup_vins_to_create.append(IcbcVinLookup(vin=vin))
        UploadedVinRecord.objects.bulk_create(
            uploaded_vin_records_to_create, ignore_conflicts=True
        )
        IcbcVinLookup.objects.bulk_create(icbc_lookup_vins_to_create)

    bytes_read = 0
    vins_and_data = []
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        bytes_read = bytes_read + record[1]
        vin = record[0]
        data = record[2]
        vins_and_data.append((vin, data))
    if vins_and_data:
        save(vins_and_data)
    return (bytes_read, end_of_file)


# returns (bytes read, eof reached)
def save_removed(prev_file_response, prev_headers, first_snapshot_date):
    def save(vins_and_data):
        vins, _ = zip(*vins_and_data)
        duplicates = set(
            IcbcDuplicateVin.objects.filter(vin__in=vins).values_list("vin", flat=True)
        )
        _, prev_tracked_records = get_untracked_and_tracked_records(
            vins_and_data, duplicates
        )
        current_file_vins = set(
            IcbcVinLookup.objects.filter(
                vin__in=prev_tracked_records.keys()
            ).values_list("vin", flat=True)
        )
        removed_df = get_removed(
            prev_tracked_records, current_file_vins, first_snapshot_date
        )
        icbc_records_to_create = []
        if removed_df is not None:
            records = removed_df.to_dict("records")
            for record in records:
                transformed_dict = get_transformed_dict(record)
                icbc_records_to_create.append(IcbcRecord(**transformed_dict))
        IcbcRecord.objects.bulk_create(icbc_records_to_create)

    bytes_read = 0
    vins_and_data = []
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(prev_file_response, prev_headers)
        if not record:
            end_of_file = True
            break
        bytes_read = bytes_read + record[1]
        vin = record[0]
        data = record[2]
        vins_and_data.append((vin, data))
    if vins_and_data:
        save(vins_and_data)
    return (bytes_read, end_of_file)


def delete_lookup_vins():
    IcbcVinLookup.objects.all().delete()
