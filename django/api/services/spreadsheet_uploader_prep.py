from decimal import Decimal
import pandas as pd
import difflib as dl
from api.services.bcngws import get_placename_matches
from api.models.regions import Regions
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

    non_num_columns = df.select_dtypes(exclude=["number"]).columns.tolist()
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

def prepare_cvp_data(df):
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in "biufc" else x.fillna(""))

    return df

def format_case(s, case='skip', ignore_list=[]):
    # Apply transformations to non-NaN values only
    mask = s.notna()

    s.loc[mask] = (
        s.loc[mask]  # I am applying this function to non-NaN values only. If you do not, they get converted from NaN to nan and are more annoying to work with.
         .astype(str)  # Convert to string
         .str.strip()  # Strip white spaces (this dataset suffers from extra tabs, lines, etc.)
    )

    if case == 'title':
        s.loc[mask] = s.loc[mask].str.title()
    elif case == 'upper':
        s.loc[mask] = s.loc[mask].str.upper()
    elif case == 'lower':
        s.loc[mask] = s.loc[mask].str.lower()
    elif case == 'sentence':
        s.loc[mask] = s.loc[mask].str.capitalize()

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
    df[['Applicant Name', 'Manufacturer']] = df[['Applicant Name', 'Manufacturer']].applymap(
    lambda x: x[0].upper() + x[1:] if isinstance(x, str) and len(x) > 1 else x.upper() if isinstance(x, str) and len(x) == 1 else x
)

    
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
        series = df[column]
        unique_vals = set(series)
        
        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
        
        typo_groups = []
        processed_values = set()
        
        for value in unique_vals:
            if value in processed_values:
                continue
            
            matches = dl.get_close_matches(value, unique_vals.difference({value}), cutoff=kwargs.get("cutoff", 0.8))
            
            if matches:
                current_group = {
                    "Typo Group": [value] + matches,
                    "Rows": []
                }
                
                current_group["Rows"].extend(map_of_values_to_indices[value])
                
                for match in matches:
                    current_group["Rows"].extend(map_of_values_to_indices[match])
                    
                processed_values.add(value)
                processed_values.update(matches)
                
                typo_groups.append(current_group)
        
        if typo_groups:
            result[column] = {
                "Similar Values Detected": {
                    "Expected Type": "We detected applicant names that sound very similar. If these names refer to the same person/entity, please replace the applicant names in your dataset to the preferred spelling to ensure consistency",
                    "Groups": typo_groups,
                    "Severity": "Warning"
                }
            }
    
    return result


def validate_phone_numbers(df, *columns, **kwargs):
    result = {}
    for column in columns:
        series = df[column]
        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
        invalid_groups = []
        
        for phone_number, indices in map_of_values_to_indices.items():
            formatted_number = str(phone_number).strip().replace('-', '')
            if len(formatted_number) != 10 or int(formatted_number[:3]) not in AREA_CODES:
                if pd.isna(formatted_number) or formatted_number == '':
                    continue
                invalid_groups.append({
                    "Invalid Phone Number": phone_number,
                    "Rows": indices
                })

        if invalid_groups:
            result[column] = {
                "Phone Number Appears Incorrect": {
                    "Expected Type": "Ensure phone numbers match the Canadian format (XXX-XXX-XXXX)",
                    "Groups": invalid_groups,
                    "Severity": "Warning"
                }
            }
    return result



def location_checker(df, *columns, columns_to_features_map={}, **kwargs):
    result = {}

    for column in columns:
        series = df[column]
        unique_values = set(series)
        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
    
        communities = set()
        features_map = columns_to_features_map.get(column, {})
        
        for category_code, feature_types in features_map.items():
            get_placename_matches(
                list(unique_values), category_code, feature_types, 
                200, 1, communities
            )
        
        names_without_match = unique_values.difference(communities)
        unrecognized_groups = []

        for name in names_without_match:
            group = {
                "Unrecognized Name": name,
                "Rows": map_of_values_to_indices[name]
            }
            unrecognized_groups.append(group)

        if unrecognized_groups:
            result[column] = {
                "Unrecognized City Names": {
                    "Expected Type": (
                        "The following city names are not in the list of geographic names. "
                        "Please double-check that these places exist or have correct spelling "
                        "and adjust your dataset accordingly."
                    ),
                    "Groups": unrecognized_groups,
                    "Severity": "Warning"
                }
            }

    return result



def email_validator(df, *columns, **kwargs):
    resolver = kwargs.get("get_resolver", None)
    if resolver:
        resolver = resolver()
    
    result = {}
    for column in columns:
        series = df[column]
        map_of_values_to_indices = get_map_of_values_to_indices(series, kwargs.get("indices_offset", 0))
        invalid_groups = []
        
        for email, indices in map_of_values_to_indices.items():
            try:
                validate_email(email, dns_resolver=resolver)
            except EmailNotValidError:
                if pd.isna(email) or email == '':
                    continue
                invalid_groups.append({
                    "Invalid Email": email,
                    "Rows": indices
                })

        if invalid_groups:
            result[column] = {
                "Possible Errors in Email Addresses": {
                    "Expected Type": "Verify email addresses are valid",
                    "Groups": invalid_groups,
                    "Severity": "Warning"
                }
            }
    return result

def validate_field_values(df, *columns, **kwargs):
    allowed_values = kwargs.get("fields_and_values")
    invalid_values = []
    
    result = {}
    delimiter = kwargs.get("delimiter")
    for column in df.columns:
        if column in allowed_values:
            indices = []
            series = df[column]
            for index, value in series.items():
                if delimiter is not None:
                    items = [item.strip() for item in value.split(delimiter)]
                
                for item in items:
                    if str(item).upper() not in (valid.upper() for valid in allowed_values[column]) and item != '' and item is not None and not pd.isna(item):
                        if index + kwargs.get("indices_offset", 0) not in indices:
                            indices.append(index + kwargs.get("indices_offset", 0))
                        if str(item) not in invalid_values:
                            invalid_values.append(str(item))
            
            if indices:
                result[column] = {
                    ', '.join(invalid_values) + " - is not in the list of expected values": {
                        "Expected Type": ', '.join(allowed_values[column]),
                        "Rows": indices,
                        "Severity": "Error"
                    }
                }
    
    return result

def region_checker(df, *columns, **kwargs):
    valid_regions = set(Regions.objects.values_list('name', flat=True))

    result = {}
    indices = []
    for column in columns:
        for index, value in df[column].items():
            values_list = [item.strip() for item in value.split(',')]
            if all(value in valid_regions for value in values_list):
                continue
            else:
                indices.append(index + kwargs.get('indices_offset', 0))

    if indices:
        result[column] = {
                    "Invalid Region": {
                        "Expected Type": "The following rows have an invalid region",
                        "Rows": indices,
                        "Severity": "Error"
                    }
                }
        
    return result