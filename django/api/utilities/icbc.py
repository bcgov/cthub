from api.constants.decoder import ICBC_FILE
import pandas as pd
import numpy as np
from datetime import datetime
import math


# returns (vin (possibly an empty string), bytes_read, data (a dict of strings to strings));
# returns an empty tuple if end of file reached
def get_record(file_response, headers):
    line = file_response.readline()
    bytes_read = len(line)
    if bytes_read == 0:
        return ()
    decoded_line = line.decode("utf-8")
    record = [item.strip() for item in decoded_line.split(ICBC_FILE.DELIMITER.value)]
    vin_index = headers.index("vin")
    vin = record[vin_index]
    if vin in ICBC_FILE.NA_VALUES.value:
        vin = ""
    vin = vin.upper()
    record[vin_index] = vin
    return (vin, bytes_read, dict(zip(headers, record)))


# vins_and_data is a list of tuples (vin, dict)
# duplicates is a set of vins
# returns (df, dict) if there are untracked vins;
# otherwise return (None, dict)
# In either case, the 2nd element is a dict of tracked vins to dicts
def get_untracked_and_tracked_records(vins_and_data, duplicates):
    df_rows = []
    tracked_records = {}
    for pair in vins_and_data:
        vin = pair[0]
        data = pair[1]
        if not vin:
            data["change"] = "untracked_missing_key"
            data["change_date"] = data["snapshot_date"]
            df_rows.append(data)
        elif vin in duplicates:
            data["change"] = "untracked_duplicate_key"
            data["change_date"] = data["snapshot_date"]
            df_rows.append(data)
        else:
            tracked_records[vin] = data
    if df_rows:
        df = pd.DataFrame(df_rows)
        return (preprocess(df), tracked_records)
    return (None, tracked_records)


# both icbc_records and file_records is a dict of vins to dicts,
# assume each vin key of icbc_records is not untracked since it comes from the icbc table
# each vin key of file_records should be a tracked vin
# returns a df if there are records to create; otherwise, return None
def get_created(icbc_records, file_records):
    # a list of dicts
    df_rows = []
    for vin, data in file_records.items():
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
            df_rows.append(data)
    if df_rows:
        df = pd.DataFrame(df_rows)
        return preprocess(df)
    return None


# both icbc_records and file_records is a dict of vins to dicts,
# assume each vin key of icbc_records is not untracked since it comes from the icbc table
# each vin key of file_records should be a tracked vin
# returns a df if there are records to create; otherwise, return None
def get_modified(icbc_records, file_records):
    # a list of dicts
    df_rows = []
    for vin, data in file_records.items():
        if vin in icbc_records:
            icbc_data = icbc_records[vin]
            last_change = icbc_data["change"]
            if last_change == "created" or last_change == "modified":
                if records_differ(icbc_data, data):
                    data["change"] = "modified"
                    data["change_date"] = data["snapshot_date"]
                    df_rows.append(data)
    if df_rows:
        df = pd.DataFrame(df_rows)
        return preprocess(df)
    return None


# compares 2 dicts
# each value in the icbc_data dict must be a non-empty string, a number, a date, or None;
# each value in the file_data dict must be a string
def records_differ(icbc_data, file_data):
    for key, value in file_data.items():
        if (
            key == "snapshot_date"
            or key == "vin"
            or key == "change"
            or key == "change_date"
        ):
            continue
        if key in icbc_data:
            icbc_value = icbc_data[key]
            if icbc_value is None:
                if value == "" or value in ICBC_FILE.NA_VALUES.value:
                    continue
                else:
                    return True
            # from this point forward, icbc_value may not be None
            if key in ICBC_FILE.NUMERIC_COLUMNS.value:
                try:
                    if int(value) != icbc_value:
                        return True
                except:
                    return True
            elif key in ICBC_FILE.DATE_COLUMNS.value:
                try:
                    if (
                        icbc_value
                        != datetime.strptime(value, ICBC_FILE.TS_FORMAT.value).date()
                    ):
                        return True
                except:
                    return True
            elif value.strip().upper() != icbc_value.strip().upper():
                return True
    return False


def get_transformed_dict(dict):
    result = {}
    for key, value in dict.items():
        if value == "" or (isinstance(value, float) and math.isnan(value)):
            result[key] = None
        else:
            result[key] = value
    return result


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


def preprocess(df):
    df.replace(ICBC_FILE.NA_VALUES.value, np.nan, inplace=True)
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
