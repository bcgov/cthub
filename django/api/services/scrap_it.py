import pandas as pd
from api.models.scrap_it import ScrapIt


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'TOP OTHER TRANSACTIONS', header=6)

    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    for _, row in df.iterrows():
        if row["VIN"] == '': continue # Skip rows without this field
        try:
            ScrapIt.objects.create(
                approval_number=row["Approval Num"],
                application_received_date=row["App Recv'd Date"],
                completion_date=row["Completion Date"],
                postal_code=row["Postal Code"],
                vin=row["VIN"],
                application_city_fuel=row["App City Fuel"],
                incentive_type=row["Incentive Type"],
                incentive_cost=row["Incentive Cost"],
                cheque_number=row["Cheque #"],
                budget_code=row["Budget Code"],
                scrap_date=row["Scrap Date"]
            )
        except Exception as error:
            print(error)
            print(row)
    return True
