from api.constants.decoder import ICBC_FILE
import pandas as pd
import math


# returns (vin (possibly None), data (a dict of strings to non-empty stripped strings, dates, integers, or None));
# returns an empty tuple if end of file reached
def get_record(file_response, headers):
    line = file_response.readline()
    if not line:
        return ()
    decoded_lines = [line.decode("utf-8")]
    number_of_quotes = decoded_lines[0].count('"')
    while number_of_quotes % 2 != 0:
        next_line = file_response.readline()
        decoded_lines.append(next_line.decode("utf-8"))
        number_of_quotes = number_of_quotes + decoded_lines[-1].count('"')
    decoded_line = "".join(decoded_lines)
    record = decoded_line.split(ICBC_FILE.DELIMITER.value)
    if len(record) != len(headers):
        raise Exception("Headers row and record length mismatch!")
    data = dict(zip(headers, record))
    for col in ICBC_FILE.COLUMNS_TO_DROP.value:
        data.pop(col, "_")
    formatted_data = get_formatted_data(data)
    return (formatted_data["vin"], formatted_data)


# data should be a dict of strings to strings
def get_formatted_data(data):
    formatted_data = {}
    for key, value in data.items():
        new_value = value.strip()
        if new_value == "" or new_value in ICBC_FILE.NA_VALUES.value:
            new_value = None
        elif key in ICBC_FILE.NUMERIC_COLUMNS.value:
            new_value = pd.to_numeric(new_value, errors="coerce", downcast="integer")
            if pd.isna(new_value):
                new_value = None
            elif isinstance(new_value, float):
                new_value = math.trunc(new_value)
        elif key in ICBC_FILE.DATE_COLUMNS.value:
            new_value = pd.to_datetime(
                new_value, yearfirst=True, utc=True, errors="coerce"
            ).date()
            if pd.isna(new_value):
                new_value = None
        elif key in ICBC_FILE.UPPER_COLUMNS.value:
            new_value = new_value.upper()
        elif key in ICBC_FILE.LOWER_COLUMNS.value:
            new_value = new_value.lower()
        elif key in ICBC_FILE.TITLE_COLUMNS.value:
            new_value = new_value.title()
        formatted_data[key] = new_value
    return formatted_data


# vins_and_data is a list of tuples (vin, dict)
# duplicates is a set of vins
# returns (list of dicts, dict of vins to data dicts)
def get_untracked_and_tracked_records(vins_and_data, duplicates):
    untracked_records = []
    tracked_records = {}
    for pair in vins_and_data:
        vin = pair[0]
        data = pair[1].copy()
        if not vin:
            data["change"] = "untracked_missing_key"
            data["change_date"] = data["snapshot_date"]
            untracked_records.append(data)
        elif vin in duplicates:
            data["change"] = "untracked_duplicate_key"
            data["change_date"] = data["snapshot_date"]
            untracked_records.append(data)
        else:
            tracked_records[vin] = data
    return (untracked_records, tracked_records)


# both icbc_records and file_records is a dict of vins to dicts,
# each vin key of icbc_records and file_records should be a tracked vin
# returns a dict of created records (vins to data dicts)
def get_created(icbc_records, file_records):
    # a list of dicts
    result = []
    for vin, data_original in file_records.items():
        data = data_original.copy()
        created = False
        if vin not in icbc_records:
            created = True
        else:
            last_change = icbc_records[vin]["change"]
            if last_change == "removed":
                created = True
        if created:
            data["change"] = "created"
            data["change_date"] = data["snapshot_date"]
            result.append(data)
    return result


# both icbc_records and file_records is a dict of vins to dicts,
# each vin key of icbc_records and file_records should be a tracked vin
# returns a dict of modified records (vins to data dicts)
def get_modified(icbc_records, file_records):
    # a list of dicts
    result = []
    for vin, data_original in file_records.items():
        data = data_original.copy()
        if vin in icbc_records:
            icbc_data = icbc_records[vin]
            last_change = icbc_data["change"]
            if last_change == "created" or last_change == "modified":
                if records_differ(icbc_data, data):
                    data["change"] = "modified"
                    data["change_date"] = data["snapshot_date"]
                    result.append(data)
    return result


# compares 2 dicts
# each value in the icbc_data dict must be a string, an integer, a date, or None;
# each value in the file_data dict must be a non-empty, stripped string, an integer, a date, or None;
def records_differ(icbc_data, file_data):
    keys_to_use = set(icbc_data).intersection(set(file_data))
    for key in keys_to_use:
        if key == "snapshot_date":
            continue
        icbc_value = icbc_data[key]
        file_value = file_data[key]
        icbc_value_is_empty = (icbc_value is None) or (
            isinstance(icbc_value, str) and icbc_value.strip() == ""
        )
        file_value_is_empty = file_value is None
        if icbc_value_is_empty and file_value_is_empty:
            continue
        if icbc_value_is_empty and not file_value_is_empty:
            return True
        if (not icbc_value_is_empty) and file_value_is_empty:
            return True
        # from this point forward, icbc_value and file_value are both not "empty"
        if key in ICBC_FILE.NUMERIC_COLUMNS.value or key in ICBC_FILE.DATE_COLUMNS.value:
            if file_value != icbc_value:
                return True
        elif file_value.upper() != icbc_value.strip().upper():
            return True
    return False
