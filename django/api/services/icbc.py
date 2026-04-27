import traceback
from datetime import datetime
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.models.icbc import IcbcRecord
from api.models.icbc_duplicate_vin import IcbcDuplicateVin
from api.models.icbc_vin_lookup import IcbcVinLookup
from api.utilities.icbc import (
    get_record,
    get_transformed_dict,
    get_untracked_and_tracked_records,
    get_created,
    get_modified,
)
from api.constants.decoder import ICBC_FILE
from django.db import connection
from django.utils import timezone


def get_icbc_ev_records(vins):
    result = {}
    records = (
        IcbcRecord.objects.filter(vin__in=vins)
        .order_by("vin", "-snapshot_date")
        .distinct("vin")
        .only(
            "vin",
            "change",
            "electric_vehicle_flag",
            "fuel_type",
            "hybrid_vehicle_flag",
            "make",
            "model",
            "model_year",
        )
    )
    for record in records:
        change = record.change
        ev_flag = record.electric_vehicle_flag
        hybrid_flag = record.hybrid_vehicle_flag
        fuel_type = record.fuel_type
        if (change == "created" or change == "modified") and (
            (ev_flag is not None and ev_flag.upper() == "Y")
            or (hybrid_flag is not None and hybrid_flag.upper() == "Y")
            or (fuel_type is not None and fuel_type.lower() == "electric")
            or (fuel_type is not None and fuel_type.lower() == "hydrogen")
            or (fuel_type is not None and fuel_type.lower() == "gasolineelectric")
        ):
            result[record.vin] = {
                "make": record.make,
                "model": record.model,
                "model_year": record.model_year,
            }
    return result


def icbc_parse_and_save(uploaded_vins_file, file_response):
    statuses = UploadedVinsFile.FileStatus
    status = uploaded_vins_file.status
    headers = uploaded_vins_file.headers
    bytes_read = 0

    try:
        if status == statuses.NEW:
            uploaded_vins_file.first_snapshot_date = get_first_snapshot_date(
                file_response, headers
            )
            uploaded_vins_file.status = statuses.SUCCESS_SAVING_FIRST_SNAPSHOT_DATE
        elif (
            status == statuses.SUCCESS_SAVING_FIRST_SNAPSHOT_DATE
            or status == statuses.SAVING_DUPLICATES_AND_LOOKUPS
        ):
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_lookup_vins_and_duplicates(file_response, headers)
                bytes_read = bytes_read + result[0]
                end_of_file = result[1]
                if end_of_file:
                    break
            if end_of_file:
                uploaded_vins_file.byte_offset = uploaded_vins_file.headers_byte_length
                uploaded_vins_file.status = (
                    statuses.SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS
                )
            else:
                uploaded_vins_file.byte_offset = (
                    uploaded_vins_file.byte_offset + bytes_read
                )
                uploaded_vins_file.status = statuses.SAVING_DUPLICATES_AND_LOOKUPS
        elif (
            status == statuses.SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS
            or status == statuses.TRACKING_REMOVED_RECORDS
        ):
            last_encountered_vin = uploaded_vins_file.last_encountered_vin
            end_of_table = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_removed(
                    last_encountered_vin, uploaded_vins_file.first_snapshot_date
                )
                last_encountered_vin = result[0]
                end_of_table = result[1]
                if end_of_table:
                    break
            uploaded_vins_file.last_encountered_vin = last_encountered_vin
            if end_of_table:
                uploaded_vins_file.status = statuses.SUCCESS_TRACKING_REMOVED_RECORDS
            else:
                uploaded_vins_file.status = statuses.TRACKING_REMOVED_RECORDS
        elif (
            status == statuses.SUCCESS_TRACKING_REMOVED_RECORDS
            or status == statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
        ):
            end_of_file = False
            for _ in range(ICBC_FILE.CHUNKS_PER_ITERATION.value):
                result = save_created_and_modified(file_response, headers)
                bytes_read = bytes_read + result[0]
                end_of_file = result[1]
                if end_of_file:
                    break
            uploaded_vins_file.byte_offset = uploaded_vins_file.byte_offset + bytes_read
            if end_of_file:
                uploaded_vins_file.status = statuses.SUCCESS
            else:
                uploaded_vins_file.status = (
                    statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
                )
    except:
        traceback.print_exc()
        if status == statuses.NEW:
            error_status = statuses.ERROR_SAVING_FIRST_SNAPSHOT_DATE
        elif (
            status == statuses.SUCCESS_SAVING_FIRST_SNAPSHOT_DATE
            or status == statuses.SAVING_DUPLICATES_AND_LOOKUPS
        ):
            error_status = statuses.ERROR_SAVING_DUPLICATES_AND_LOOKUPS
        elif (
            status == statuses.SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS
            or status == statuses.TRACKING_REMOVED_RECORDS
        ):
            error_status = statuses.ERROR_TRACKING_REMOVED_RECORDS
        elif (
            status == statuses.SUCCESS_TRACKING_REMOVED_RECORDS
            or status == statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
        ):
            error_status = statuses.ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS
        UploadedVinsFile.objects.filter(id=uploaded_vins_file.id).using("other").update(
            status=error_status, update_timestamp=timezone.now()
        )
        raise Exception()

    uploaded_vins_file.save()


# returns first snapshot date
def get_first_snapshot_date(file_response, headers):
    first_snapshot_date = None
    while first_snapshot_date is None:
        record = get_record(file_response, headers)
        data = record[2]
        try:
            first_snapshot_date = datetime.strptime(
                data["snapshot_date"], ICBC_FILE.TS_FORMAT.value
            ).date()
        except:
            pass
    return first_snapshot_date


# returns (bytes read, eof reached)
def save_lookup_vins_and_duplicates(file_response, headers):
    def save_dups(dup_vins):
        records = []
        for vin in dup_vins:
            records.append(IcbcDuplicateVin(vin=vin))
        IcbcDuplicateVin.objects.bulk_create(records, ignore_conflicts=True)

    def save(vins):
        dup_vins = IcbcVinLookup.objects.filter(vin__in=vins).values_list(
            "vin", flat=True
        )
        if dup_vins:
            save_dups(dup_vins)
        records = []
        for vin in vins:
            records.append(IcbcVinLookup(vin=vin))
        IcbcVinLookup.objects.bulk_create(records, ignore_conflicts=True)

    bytes_read = 0
    seen_vins = set()
    dup_vins = set()
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        bytes_read = bytes_read + record[1]
        vin = record[0]
        if vin:
            if vin in seen_vins:
                dup_vins.add(vin)
            seen_vins.add(vin)
    if dup_vins:
        save_dups(dup_vins)
    save(seen_vins)
    return (bytes_read, end_of_file)


# returns (last encountered vin, end of table reached)
def save_removed(last_encountered_vin, first_snapshot_date):
    last_encountered_vin_to_use = last_encountered_vin
    filter = {}
    if last_encountered_vin_to_use is not None:
        filter["vin__gt"] = last_encountered_vin_to_use
    icbc_records = list(
        IcbcRecord.objects.filter(**filter)
        .order_by("vin", "-snapshot_date")
        .distinct("vin")[: ICBC_FILE.CHUNK_SIZE.value]
    )
    if len(icbc_records) == 0:
        truncate_vin_lookups()
        return (last_encountered_vin_to_use, True)
    else:
        last_encountered_vin_to_use = icbc_records[-1].vin
    vins_dict = {}
    for record in icbc_records:
        change = record.change
        if change == "created" or change == "modified":
            vins_dict[record.vin] = record
    vins = set(vins_dict)
    duplicates = set(
        IcbcDuplicateVin.objects.filter(vin__in=vins).values_list("vin", flat=True)
    )
    refined_vins = vins.difference(duplicates)
    found_vins = set(
        IcbcVinLookup.objects.filter(vin__in=refined_vins).values_list("vin", flat=True)
    )
    removed_vins = refined_vins.difference(found_vins)
    removed_records = []
    for vin in removed_vins:
        record = vins_dict[vin]
        record.record_id = None
        record.change = "removed"
        record.change_date = first_snapshot_date
        removed_records.append(record)
    if removed_records:
        IcbcRecord.objects.bulk_create(removed_records)
    return (last_encountered_vin_to_use, False)


def truncate_vin_lookups():
    # django queryset does not have a "truncate" method, so we do:
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE icbc_vin_lookup RESTART IDENTITY")


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
            .order_by("vin", "-snapshot_date")
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
        for vin in tracked_records.keys():
            uploaded_vin_records_to_create.append(UploadedVinRecord(vin=vin))
        UploadedVinRecord.objects.bulk_create(
            uploaded_vin_records_to_create, ignore_conflicts=True
        )

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
