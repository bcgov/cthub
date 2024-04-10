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


def applicant_type(row):
    if isinstance((row["Fleet"]), str):
        return "Fleet"
    elif isinstance((row["Individual"]), str):
        return "Individual"
    else:
        return ""


def prepare_speciality_use_vehicle_incentives(df):

    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    num_columns = df.select_dtypes(include=["number"]).columns.tolist()
    df[num_columns] = df[num_columns].fillna(0)

    non_num_columns = df.columns.difference(num_columns)
    df[non_num_columns] = df[non_num_columns].fillna("")

    df["Applicant Type"] = df.apply(lambda row: applicant_type(row), axis=1)

    if "Fleet" in df.columns:
        df = df.drop(columns=["Fleet"])

    if "Individual" in df.columns:
        df = df.drop(columns=["Individual"])

    return df
