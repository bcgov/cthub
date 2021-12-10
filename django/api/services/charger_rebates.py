import pandas as pd
from api.models.charger_rebates import ChargerRebates


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'Raw Data')
    df.drop(df.columns.difference([
        "Organization",
        "MLA",
        "Region",
        "City",
        "Address",
        "Number of Fast Charging Stations",
        "In service date",
        "Announced?",
        "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)",
        "Notes",
    ]), 1, inplace=True)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df['B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)'].replace(
        to_replace=['$', ''],
        value=True,
        inplace=True
    )
    df['B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)'].replace(
        to_replace=[',', ''],
        value=True,
        inplace=True
    )
    df.fillna('')

    for _, row in df.iterrows():
        try:
            ChargerRebates.objects.create(
                organization=row["Organization"],
                region=row["MLA"],
                city=row["Region"],
                address=row["City"],
                number_of_fast_charging_stations=row["Address"],
                in_service_date=row["Number of Fast Charging Stations"],
                expected_in_service_date=row["In service date"],
                announced=row["Announced?"],
                rebate_paid=row["B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)"],
                notes=row["Notes"]
            )
        except Exception as error:
            print(error)
            print(row)
    return True
