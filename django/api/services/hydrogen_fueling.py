import pandas as pd
from api.models.hydrogen_fueling import HydrogrenFueling


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    row_count = 1
    df = pd.read_excel(excel_file, 'Station_Tracking')
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))
    df['700 Bar'].replace(
        to_replace=['NO', 'N'],
        value=False,
        inplace=True
    )
    df['700 Bar'].replace(
        to_replace=['YES', 'Y'],
        value=True,
        inplace=True
    )
    df['350 Bar'].replace(
        to_replace=['NO', 'N'],
        value=False,
        inplace=True
    )
    df['350 Bar'].replace(
        to_replace=['YES', 'Y'],
        value=True,
        inplace=True
    )
    try:
        for _, row in df.iterrows():
            row_count +=1
            HydrogrenFueling.objects.create(
                station_number=row["Station Number"],
                rfp_close_date=row["RFP Close Date"],
                station_name=row["Station Name"],
                street_address=row["Street Address"],
                city=row["City"],
                postal_code=row["Postal Code"],
                proponent=row["Proponent"],
                location_partner=row["Location Partner (Shell/7-11/etc.)"],
                capital_funding_awarded=row["Capital Funding Awarded"],
                om_funding_potential=row["O&M Funding Potential"],
                daily_capacity=row["Daily Capacity (kg/day)"],
                bar_700=row["700 Bar"],
                bar_350=row["350 Bar"],
                status=["Status"],
                number_of_fueling_positions=row["# of Fuelling Positions"],
                operational_date=row["Operational Date "],
                opening_date=row["Opening Date"],
                total_capital_cost=row["Total Capital Cost"]  
            )
    except Exception as error:
        return (error,'data',row_count)  
    return True
