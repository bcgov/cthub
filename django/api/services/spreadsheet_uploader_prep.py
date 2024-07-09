from decimal import Decimal
import pandas as pd
import difflib as dl
from api.services.bcngws import get_placename_matches
from email_validator import validate_email, EmailNotValidError
from api.utilities.series import get_map_of_values_to_indices
from api.constants.misc import AREA_CODES

def prepare_arc_project_tracking(df):
    df["Publicly Announced"] = df["Publicly Announced"].replace(
        {"No": False, "N": False, "Yes": True, "Y": True}
    )
    return df


def prepare_hydrogen_fleets(df):
    df.applymap(lambda s: s.upper() if type(s) == str else s)
    df.apply(lambda x: x.fillna(0) if x.dtype.kind in "biufc" else x.fillna(""))
    return df

def prepare_hydrogen_fueling(df):

    decimal_columns = ["Capital Funding Awarded", "O&M Funding Potential"]

    for column in ["700 Bar", "350 Bar"]:
        df[column].replace(to_replace=["NO", "N"], value=False, inplace=True)
        df[column].replace(to_replace=["YES", "Y"], value=True, inplace=True)

    for field in decimal_columns:
        try:
            df[field] = df[field].apply(
                lambda x: round(Decimal(x), 2) if pd.notnull(x) else None
            )
        except:
            print({f"{field} Should be a header row"})
    return df


def prepare_ldv_rebates(df):
    replacements = {
        "CASL Consent": {"YES": True, "Y": True, "NO": False, "N": False},
        "Delivered": {
            "YES": True,
            "Y": True,
            "NO": False,
            "N": False,
            "OEM": False,
            "INCENTIVE_FUNDS_AVAILABLE": False,
        },
        "Consent to Contact": {"YES": True, "Y": True, "NO": False, "N": False},
    }

    for column, replacement_dict in replacements.items():
        df[column].replace(replacement_dict, inplace=True)

    df.fillna("")

    return df


def prepare_public_charging(df):

    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in "biufc" else x.fillna(""))

    df["Pilot Project (Y/N)"].replace(to_replace=["NO", "N"], value=False, inplace=True)
    df["Pilot Project (Y/N)"].replace(to_replace=["YES", "Y"], value=True, inplace=True)

    return df


def prepare_scrap_it(df):

    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in "biufc" else x.fillna(""))

    return df

def prepare_go_electric_rebates(df):

    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    num_columns = df.select_dtypes(include=["number"]).columns.tolist()
    df[num_columns] = df[num_columns].fillna(0)

    non_num_columns = df.columns.difference(num_columns)
    df[non_num_columns] = df[non_num_columns].fillna("")
    format_dict = {
        'title': ['Approvals', 'Applicant Name', 'Category', 
                  'Fleet/Individuals',  'Rebate adjustment (discount)', 
                  'Manufacturer', 'City'],
        'upper': ['Model', 'Postal code', 'VIN Number'],
        'lower': ['Email'],
        'skip': ['Phone Number'],
        'sentence': ['Notes'],
}
    for key in format_dict:
        df[format_dict[key]] = df[format_dict[key]].apply(format_case, case = key)

    make_names_consistent(df)
    make_prepositions_consistent(df)
    adjust_ger_manufacturer_names(df)
    return df

def format_case(s, case = 'skip', ignore_list = []):
    s[s.notna()] = (
        s[s.notna()] # I am applying this function to non NaN values only. If you do not, they get converted from NaN to nan and are more annoying to work with.
         .astype(str) # Convert to string
         .str.strip() # Strip white spaces (this dataset suffers from extra tabs, lines, etc.)
        )
    if case == 'title':
        s = s.str.title()
    elif case == 'upper':
        s = s.str.upper()
    elif case == 'lower':
        s = s.str.lower()
    elif case == 'sentence':
        ##filter out the temporary null records before changing to sentence case
        s = s[s != 'TEMP_NULL'].str.capitalize()
    elif case == 'skip':
        pass

    return s

def make_names_consistent(df):
    """
    This step is done after formatting because people use all kinds of cases (`LTD`, `ltd', 'LIMITED'`, etc.).

    To `Ltd.` from:
        - `Ltd`
        - `Limited`
        - `Limited.`

    To `Inc.` from:
        - `Inc`
        - `Incorporated`

    - From `Dba` to `DBA` i.e. "doing business as"
    
    """
    consistent_name_dict = (
    dict.fromkeys([
        '\\bLtd(?!\\.)\\b', # Matches word "Ltd" not followed by "."
        'Limited$', # Matches "Limited" at the end of the string
        'Limited\\.$', # Matches "Limited." at the end of the string
        ', Ltd.'
        ], 'Ltd.') |
    dict.fromkeys([
        '\\bInc(?!\\.)\\b', # Matches "Inc" not followed by "."
        'Incorporated'], 'Inc.') |
    {', Inc.': ' Inc.',
    '(?i)\\bdba\\b': 'DBA'} # Matches word "dba" regardless of case
)
    df[['Applicant Name', 'Manufacturer']] = df[['Applicant Name', 'Manufacturer']].replace(
        consistent_name_dict,
        regex=True)

def make_prepositions_consistent(df):
    df[['Applicant Name', 'Manufacturer']] = df[['Applicant Name', 'Manufacturer']].replace(
    dict.fromkeys(
    ['(?i)\\bbc(?=\\W)', # Matches word "bc" regardless of case
     '(?i)\\bb\\.c\\.(?=\\W)'], 'BC'), # Matches word "b.c." regardless of case
    regex=True
    ).replace(
        {'BC Ltd.': 'B.C. Ltd.',
         '\\bOf(?=\\W)': 'of',
         '\\bAnd(?=\\W)': 'and', # Matches word "And"
         '\\bThe(?=\\W)': 'the',
         '\\bA(?=\\W)': 'a',
         '\\bAn(?=\\W)': 'an'},
        regex=True
    )
    ##The first letter should be capitalized
    df[['Applicant Name', 'Manufacturer']] = df[['Applicant Name', 'Manufacturer']
        ].applymap(lambda x: x[0].upper() + x[1:])
    
def adjust_ger_manufacturer_names(df):
    """""
    This function is currently GER specific updating the manufacturer names to have casing that makes more sense
    since currently all manufacturer column entries are set to sentence casing.

    """""

    name_replacements = {
        'International Ic Bus': 'International IC Bus',
        'Lightning Emotors': 'Lightning eMotors',
        'Avro Gse': 'Avro GSE',
        'Bmw': 'BMW',
        'Ego': 'EGO',
        'Sc Carts': 'SC Carts'
    }

    df[['Manufacturer']] = df[['Manufacturer']].replace(name_replacements, regex=False)


def typo_checker(df, *columns, **kwargs):
    result = {}
    for column in columns:
        indices = []
        series = df[column]
        unique_vals = set(series)

        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
        for value in unique_vals:
            singleton = set()
            singleton.add(value)
            matches = dl.get_close_matches(
                value,
                unique_vals.difference(singleton),
                cutoff = kwargs["cutoff"]
            )
            if matches:
                indices_to_add = map_of_values_to_indices[value]
                indices.extend(indices_to_add)
        if indices:
            result[column] = sorted(list(set(indices)))
    return result


def get_validation_error_rows(errors):
    row_numbers = set()
    for error in errors:
        try:
            row_number = int(error.split()[1][:-1])
            row_numbers.add(row_number)
        except (IndexError, ValueError):
            continue
    return row_numbers


def validate_phone_numbers(df, *columns, **kwargs):
    result = {}
    for column in columns:
        indices = []
        series = df[column]
        for index, phone_number in series.items():
            formatted_number = str(phone_number).strip().replace('-', '')
            if formatted_number == '' or len(formatted_number) != 10 or int(formatted_number[:3]) not in AREA_CODES:
                indices.append(index + kwargs.get("indices_offset", 0))
        if indices:
            result[column] = indices
    return result


def location_checker(df, *columns, **kwargs):
    result = {}
    for column in columns:
        indices = []
        series = df[column]
        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
        values = series.to_list()
        unique_values = set(series)

        communities = set()
        # populate communities by calling the bcngws API with the values:
        get_placename_matches(values, 200, 1, communities)
        names_without_match = unique_values.difference(communities)
        for name in names_without_match:
            indices_to_add = map_of_values_to_indices[name]
            indices.extend(indices_to_add)
        if indices:
            result[column] = sorted(list(set(indices)))
    return result


def email_validator(df, *columns, **kwargs):
    result = {}
    for column in columns:
        indices = []
        series = df[column]
        for index, value in series.items():
            try:
                validate_email(value)
            except EmailNotValidError:
                indices.append(index + kwargs.get("indices_offset", 0))
        if indices:
            result[column] = indices
    return result