import pandas as pd
from api.models.public_charging import PublicCharging


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    row_count = 3
    df = pd.read_excel(excel_file, 'Project_applications', header=2)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))
    df['Pilot Project (Y/N)'].replace(
        to_replace=['NO', 'N'],
        value=False,
        inplace=True
    )
    df['Pilot Project (Y/N)'].replace(
        to_replace=['YES', 'Y'],
        value=True,
        inplace=True
    )
    try:
        for _, row in df.iterrows():
            row_count += 1
            PublicCharging.objects.create(
                applicant_name=row["Applicant Name"],
                address=row["Address"],
                charging_station_info=row["Charging Station Info"],
                between_25kw_and_50kw=row[">25kW; <50kW"],
                between_50kw_and_100kw=row[">50kW; <100kW"],
                over_100kw=row[">100kW "],
                level_2_units=row["Level 2 (# of units/stations)"],
                level_2_ports=row["Level 2 (# of ports)"],
                estimated_budget=row["Estimated Budget"],
                adjusted_rebate=row["Adjusted Rebate "],
                rebate_percent_maximum=row["Rebate % Maximum "],
                pilot_project=row["Pilot Project (Y/N)"],
                region=row["Region"],
                organization_type=row["Organization Type"],
                project_status=row["Project Status"],
                review_number=row["Review Number"],
                rebate_paid=row["Paid out rebate amount"],
            )
    except Exception as error:
        return (error,'data',row_count) 
    return True
