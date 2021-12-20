import pandas as pd
from api.models.charger_rebates import ChargerRebates


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'Updated', header=2)
    df.drop(df.columns.difference([
        "Organization",
        "MLA",
        "Region",
        "City",
        "Address",
        "Number of Fast Charging Stations",
        "In service date",
        "Expected in service date",
        "Announced?",
        "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)",
        "Notes",
    ]), 1, inplace=True)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    # df.fillna('')
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    for _, row in df.iterrows():
        try:
            ChargerRebates.objects.create(
                organization=row["Organization"],
                region=row["Region"],
                city=row["City"],
                address=row["Address"],
                number_of_fast_charging_stations=row["Number of Fast Charging Stations"],
                in_service_date=row["In service date"],
                expected_in_service_date=row["Expected in service date"],
                announced=row["Announced?"],
                rebate_paid=row["B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)"],
                notes=row["Notes"]
            )
        except Exception as error:
            print(error)
            print(row)
    return True
