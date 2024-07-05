from decimal import Decimal
import numpy as np
import pandas as pd
import difflib as dl
from api.services.bcngws import get_placename_matches

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


def typo_checker(df, column, kwargs):
    """
    Check for similar words in a single Pandas Series.

    Parameters
    ----------
    c : Similarity cutoff, higher is more similar

    Returns
    -------
    dict
        A dictionary with grouped similar words and their line numbers

    """
    s = df[column].dropna()
    header_rows = kwargs["header"]
    if isinstance(s, pd.Series) is False:
        raise Exception('Function argument "s" has to be Pandas Series type')

    if s.nunique() == 1:
        raise Exception('Function argument "s" contains only one unique value, there is nothing to compare')
    elif s.empty:
        raise Exception('Function argument "s" is empty, there is nothing to compare')

    unique_vals = list(set(s))  # Get all unique values from the series
    unique_vals.sort(reverse=True)  # Sort them to check for duplicates later

    parent = {val: val for val in unique_vals}  # Union-find data structure

    def find(val):
        if parent[val] != val:
            parent[val] = find(parent[val])
        return parent[val]

    def union(val1, val2):
        root1 = find(val1)
        root2 = find(val2)
        if root1 != root2:
            parent[root2] = root1

    for value in unique_vals:
        matches = dl.get_close_matches(
            value,  # Value to compare
            unique_vals[:unique_vals.index(value)] + unique_vals[unique_vals.index(value)+1:],  # All other values to compare value to
            cutoff = kwargs["cutoff"]  # Similarity cutoff score, higher values mean more similar
        )

        for match in matches:
            union(value, match)

    groups = {}
    for value in unique_vals:
        root = find(value)
        if root not in groups:
            groups[root] = {
                'names': set(),
                'lines': set()
            }
        groups[root]['names'].add(value)
        groups[root]['lines'].update(s[s == value].index.tolist())

    # Filter out groups that don't have any matches and adjust line numbers to start at 1 plus whatever the header is
    filtered_groups = {", ".join(sorted([str(line + header_row + 1) for line in group['lines']])): sorted(group['names'])
                   for group in groups.values() if len(group['names']) > 1}
    return 'typos', filtered_groups if filtered_groups else None


def get_validation_error_rows(errors):
    row_numbers = set()
    for error in errors:
        try:
            row_number = int(error.split()[1][:-1])
            row_numbers.add(row_number)
        except (IndexError, ValueError):
            continue
    return row_numbers

def validate_phone_numbers(df, column, kwargs):
    header_rows = kwargs["header"]
    phone_errors = {}

    area_codes = [
        587, 368, 403, 825, 780,  # Alberta
        236, 672, 604, 778, 250,  # British Columbia
        584, 431, 204,            # Manitoba
        506,                      # New Brunswick
        709,                      # Newfoundland
        867,                      # Northwest Territories
        782, 902,                 # Nova Scotia
        867,                      # Nunavut
        365, 226, 647, 519, 289, 742, 807, 548, 753, 249, 683, 437, 905, 343, 613, 705, 416,  # Ontario
        782, 902,                 # Prince Edward Island
        450, 418, 873, 468, 367, 819, 579, 581, 438, 354, 514, 263,  # Quebec
        306, 474, 639,            # Saskatchewan
        867                       # Yukon
    ]

    for index, row in df.iterrows():

        number = row[column]
        formatted_number = str(number).strip().replace('-', '')

        if formatted_number == '':
            phone_errors[f"{index + 1}"] = "Had an empty phone number"

        elif len(formatted_number) != 10 or int(formatted_number[:3]) not in area_codes:
            phone_errors[f"{index + header_rows + 1}"] = f"Had an invalid phone number - '{number}'."

    return 'phone_errors', phone_errors if phone_errors else None


def location_checker(df, column, kwargs):
    names_dict = df[column].to_dict()
    header_rows = kwargs["header"]
    communities = []
    # Send request to API with list of names, returns all the communities that somewhat matched
    get_placename_matches(names_dict, 200, 1, communities)
    locations_set = set(communities)
    # Find names that don't have a match in the locations_set
    names_without_match = {
    row + header_rows + 1: f"{name} was not found in our geographic names dataset"
    for row, name in names_dict.items()
    if name not in locations_set
}
    return 'Location Not Found', names_without_match if names_without_match else None

