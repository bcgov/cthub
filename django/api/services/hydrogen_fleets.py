import pandas as pd
from api.models.charger_rebates import ChargerRebates


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'Fleets')
    df.drop(df.columns.difference([
        "Application #",
        "Fleet #",
        "Application Date",
        "Organization Name"
        "Fleet Name",
        "Street Address",
        "City",
        "Postal Code",
        "VIN",
        "Make",
        "Model",
        "Year",
        "Purchase Date",
        "Dealer Name",
        "Rebate Amount"
    ]), 1, inplace=True)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    # df.fillna('')
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    for _, row in df.iterrows():
        try:
            ChargerRebates.objects.create(
                application_number=row["Application #"],
                fleet_number=row["Fleet #"],
                application_date=row["Application Date"],
                organization_name=row["Organization Name"],
                fleet_name=row["Fleet Name"],
                street_address=row["Street Address"],
                city=row["City"],
                postal_code=row["Postal Code"],
                vin=row["VIN"],
                make=row["Make"],
                model=row["Model"],
                year=row["Year"],
                purchase_date=row["Purchase Date"],
                dealer_name=row["Dealer Name"],
                rebate_amount=row["Rebate Amount"]
            )
        except Exception as error:
            print(error)
            print(row)
    return True
