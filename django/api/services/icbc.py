import traceback
from api.models.uploaded_vins_file import UploadedVinsFile
from api.models.uploaded_vin_record import UploadedVinRecord
from api.models.icbc import IcbcRecord
from api.models.icbc_duplicate_vin import IcbcDuplicateVin
from api.models.icbc_vin_lookup import IcbcVinLookup
from api.utilities.icbc import (
    get_record,
    get_untracked_and_tracked_records,
    get_created,
    get_modified,
)
from api.constants.decoder import ICBC_FILE, FILE_PROCESSING_DIRECTORY
from django.db import connection
from django.utils import timezone
from datetime import datetime


def temp1(vins):
    print("in temp1")
    print(f"number of vins received: {len(vins)}")
    result = list(
        IcbcRecord.objects.filter(vin__in=vins)
        .order_by("vin", "-change_date")
        .distinct("vin")
        .values()
    )
    print(f"result length: {len(result)}")
    return result


def temp2(vins):
    print("in temp2")
    print(f"number of vins received: {len(vins)}")
    result = list(
        IcbcRecord.objects.filter(vin__in=vins)
        .order_by("vin", "-change_date")
        .distinct("vin")
        .values()[:5000]
    )
    print(f"result length: {len(result)}")
    return result


def temp3(vins):
    print("in temp3")
    print(f"number of vins received: {len(vins)}")
    my_dict = {}
    for vin in vins:
        my_dict[vin] = None
    keys = list(my_dict.keys())
    result = list(
        IcbcRecord.objects.filter(vin__in=keys)
        .order_by("vin", "-change_date")
        .distinct("vin")
        .values()
    )
    print(f"result length: {len(result)}")
    return result


def get_icbc_ev_records(vins):
    result = {}
    records = list(
        IcbcRecord.objects.filter(vin__in=vins)
        .order_by("vin", "-change_date")
        .distinct("vin")
        .values(
            "vin",
            "change",
            "electric_vehicle_flag",
            "fuel_type",
            "hybrid_vehicle_flag",
            "make",
            "model",
            "model_year",
            "vehicle_registration_date",
        )
    )
    for record in records:
        change = record["change"]
        ev_flag = record["electric_vehicle_flag"]
        hybrid_flag = record["hybrid_vehicle_flag"]
        fuel_type = record["fuel_type"]
        if (change == "created" or change == "modified") and (
            (ev_flag is not None and ev_flag.upper() == "Y")
            or (hybrid_flag is not None and hybrid_flag.upper() == "Y")
            or (fuel_type is not None and fuel_type.lower() == "electric")
            or (fuel_type is not None and fuel_type.lower() == "hydrogen")
            or (fuel_type is not None and fuel_type.lower() == "gasolineelectric")
        ):
            result[record["vin"]] = {
                "make": record["make"],
                "model": record["model"],
                "model_year": record["model_year"],
                "registration_date": (
                    record["vehicle_registration_date"].strftime("%Y-%m-%d")
                    if record["vehicle_registration_date"]
                    else None
                ),
            }
    return result


def icbc_parse_and_save(uploaded_vins_file, file_response):
    statuses = UploadedVinsFile.FileStatus
    status = uploaded_vins_file.status
    headers = uploaded_vins_file.headers

    try:
        if status == statuses.NEW:
            write_to_disk(file_response, uploaded_vins_file.filename)
            uploaded_vins_file.status = statuses.SUCCESS_WRITING_FILE_TO_DISK
        elif status == statuses.SUCCESS_WRITING_FILE_TO_DISK:
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
                end_of_file = save_lookup_vins_and_duplicates(file_response, headers)
                if end_of_file:
                    break
            if end_of_file:
                uploaded_vins_file.byte_offset = uploaded_vins_file.headers_byte_length
                uploaded_vins_file.status = (
                    statuses.SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS
                )
            else:
                uploaded_vins_file.byte_offset = file_response.tell()
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
                print(
                    f"started processing a chunk at {(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}"
                )
                end_of_file = save_created_and_modified(file_response, headers)
                print(
                    f"finished processing a chunk at {(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}"
                )
                if end_of_file:
                    break
            uploaded_vins_file.byte_offset = file_response.tell()
            if end_of_file:
                uploaded_vins_file.status = statuses.SUCCESS
            else:
                uploaded_vins_file.status = (
                    statuses.TRACKING_CREATED_AND_MODIFIED_RECORDS
                )
    except:
        traceback.print_exc()
        if status == statuses.NEW:
            error_status = statuses.ERROR_WRITING_FILE_TO_DISK
        elif status == statuses.SUCCESS_WRITING_FILE_TO_DISK:
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


def write_to_disk(file_response, file_name):
    file_path = f"{FILE_PROCESSING_DIRECTORY}/{file_name}"
    with open(file_path, "wb") as f:
        for chunk in file_response.stream():
            f.write(chunk)


# returns first snapshot date
def get_first_snapshot_date(file_response, headers):
    first_snapshot_date = None
    while first_snapshot_date is None:
        record = get_record(file_response, headers)
        data = record[1]
        first_snapshot_date = data.get("snapshot_date")
    return first_snapshot_date


# returns eof reached
def save_lookup_vins_and_duplicates(file_response, headers):
    def save_dups(dup_vins):
        records = []
        for vin in dup_vins:
            records.append(IcbcDuplicateVin(vin=vin))
        IcbcDuplicateVin.objects.bulk_create(records, ignore_conflicts=True)

    def save(vins):
        dup_vins = set(
            IcbcVinLookup.objects.filter(vin__in=vins).values_list("vin", flat=True)
        )
        if dup_vins:
            save_dups(dup_vins)
        records = []
        for vin in vins:
            records.append(IcbcVinLookup(vin=vin))
        IcbcVinLookup.objects.bulk_create(records, ignore_conflicts=True)

    seen_vins = set()
    dup_vins = set()
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        vin = record[0]
        if vin:
            if vin in seen_vins:
                dup_vins.add(vin)
            seen_vins.add(vin)
    if dup_vins:
        save_dups(dup_vins)
    save(seen_vins)
    return end_of_file


# returns (last encountered vin, end of table reached)
def save_removed(last_encountered_vin, first_snapshot_date):
    last_encountered_vin_to_use = last_encountered_vin
    filter = {"vin__isnull": False}
    if last_encountered_vin_to_use is not None:
        filter["vin__gt"] = last_encountered_vin_to_use
    icbc_records = list(
        IcbcRecord.objects.filter(**filter)
        .order_by("vin", "-change_date")
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


# returns eof reached
def save_created_and_modified(file_response, headers):
    def save(vins_and_data):
        vins, _ = zip(*vins_and_data)
        duplicates = set(
            IcbcDuplicateVin.objects.filter(vin__in=vins).values_list("vin", flat=True)
        )
        untracked_records, tracked_records_dict = get_untracked_and_tracked_records(
            vins_and_data, duplicates
        )
        tracked_vins = list(tracked_records_dict.keys())
        print(f"first 25 tracked vins: {tracked_vins[:25]}")
        print(
            f"beginning read icbc records at {(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}"
        )
        icbc_records = list(
            IcbcRecord.objects.filter(vin__in=tracked_vins)
            .order_by("vin", "-change_date")
            .distinct("vin")
            .values()
        )
        print(
            f"read icbc records finished at {(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}"
        )
        print(f"number of icbc records read: {len(icbc_records)}")
        icbc_records_dict = {}
        for record in icbc_records:
            icbc_records_dict[record["vin"]] = record
        created_records = get_created(icbc_records_dict, tracked_records_dict)
        modified_records = get_modified(icbc_records_dict, tracked_records_dict)
        icbc_records_to_create = []
        for collections in [untracked_records, created_records, modified_records]:
            for dict in collections:
                icbc_records_to_create.append(IcbcRecord(**dict))
        IcbcRecord.objects.bulk_create(icbc_records_to_create)
        uploaded_vin_records_to_create = []
        for vin in tracked_vins:
            uploaded_vin_records_to_create.append(UploadedVinRecord(vin=vin))
        UploadedVinRecord.objects.bulk_create(
            uploaded_vin_records_to_create, ignore_conflicts=True
        )

    vins_and_data = []
    end_of_file = False
    for _ in range(ICBC_FILE.CHUNK_SIZE.value):
        record = get_record(file_response, headers)
        if not record:
            end_of_file = True
            break
        vins_and_data.append(record)
    if vins_and_data:
        save(vins_and_data)
    return end_of_file
