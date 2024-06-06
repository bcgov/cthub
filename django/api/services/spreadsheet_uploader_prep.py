from decimal import Decimal
import numpy as np
import pandas as pd


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
        'skip': ['Phone Number']
}
    for key in format_dict:
        df[format_dict[key]] = df[format_dict[key]].apply(format_case, case = key)

    make_names_consistent(df)
    
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
