import pandas as pd
from api.models.arc_project_tracking import ARCProjectTracking


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    row_count = 1 #starting count, ie headers
    df = pd.read_excel(excel_file, 'Project_Tracking')

    df.drop(df.columns.difference([
        "Funding Call",
        "Proponent",
        "Ref #",
        "Project Title",
        "Primary Location",
        "Status",
        "ARC Funding",
        "Funds Issued",
        "Start Date",
        "Completion Date",
        "Total Project Value",
        "ZEV Sub-Sector",
        "On-Road/Off-Road",
        "Fuel Type",
        "Publicly Announced"
    ]), axis=1, inplace=True)

    df['Publicly Announced'].replace(
        to_replace=['No', 'N'],
        value=False,
        inplace=True
    )

    df['Publicly Announced'].replace(
        to_replace=['Yes', 'Y'],
        value=False,
        inplace=True
    )

    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    try:
        for _, row in df.iterrows():
            if row["Publicly Announced"] == '': continue # Skip rows without this field
            row_count += 1
            ARCProjectTracking.objects.create(
                funding_call=row["Funding Call"],
                proponent=row["Proponent"],
                reference_number=row["Ref #"],
                project_title=row["Project Title"],
                primary_location=row["Primary Location"],
                status=row["Status"],
                arc_funding=row["ARC Funding"],
                funds_issued=row["Funds Issued"],
                start_date=row["Start Date"],
                completion_date=row["Completion Date"],
                total_project_value=row["Total Project Value"],
                zev_sub_sector=row["ZEV Sub-Sector"],
                on_road_off_road=row["On-Road/Off-Road"],
                fuel_type=row["Fuel Type"],
                publicly_announced=row["Publicly Announced"]
            )
    except Exception as error:
        return (error, 'data', row_count)
    return True
