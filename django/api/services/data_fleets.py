import pandas as pd
from api.models.data_fleets import DataFleets


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def import_from_xls(excel_file):
    row_count = 1
    df = pd.read_excel(excel_file, 'Data Fleets')
    df.drop(df.columns.difference([
        "Current Stage",
        "Rebate Value",
        "Legal Name of your Organization/Fleet: ",
        "Your business Category",
        "City:*",
        "Postal Code:*",
        "Applicant First Name",
        "Applicant Last Name",
        "Email Address:*",
        "Fleet Size All",
        "Fleet Size Light-duty",
        "Total number of EVs?",
        "Total number of light-duty EVs?",
        "PHEV's",
        "EVSE's?",
        "Average daily travel distance?",
        "Which component are you applying for?*",
        "Estimated cost",
        "Which type of charger are you installing?",
        "How many Level 2 Charging Stations are you applying for",
        "How many Level 3/DC Fast Charging Stations are you applying for",
        '"Application Form Fleets" completion date/time',
        "Pre-Approval Date",
        "Deadline",
        "Application Number",
        "Potential Rebate"
    ]), axis=1, inplace=True)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)

    # df.fillna('')
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    for _, row in df.iterrows():
        row_count += 1
        try:
            DataFleets.objects.create(
                current_stage=row["Current Stage"],
                rebate_value=row["Rebate Value"],
                legal_name_of_organization_fleet =row["Legal Name of your Organization/Fleet: "],
                business_category=row["Your business Category"],
                city=row["City:*"],
                postal_code=row["Postal Code:*"],
                applicant_first_name=row["Applicant First Name"],
                applicant_last_name =row["Applicant Last Name"],
                email_address=row["Email Address:*"],
                fleet_size_all=row["Fleet Size All"],
                fleet_size_light_duty=row["Fleet Size Light-duty"],
                total_number_of_evs=row["Total number of EVs?"],
                total_number_of_light_duty_evs=row["Total number of light-duty EVs?"],
                phev=row["PHEV's"],
                evse=row["EVSE's?"],
                average_daily_travel_distance=row["Average daily travel distance?"],
                component_being_applyied_for=row["Which component are you applying for?*"],
                estimated_cost=row["Estimated cost"],
                type_of_charger_being_installing=row["Which type of charger are you installing?"],
                number_of_Level_2_Charging_Stations_being_applying_for=row["How many Level 2 Charging Stations are you applying for"],
                number_of_level_3_dc_fast_charging_stations_being_applying_for=row["How many Level 3/DC Fast Charging Stations are you applying for"],
                application_form_fleets_completion_date_time=row['"Application Form Fleets" completion date/time'],
                pre_approval_date=row["Pre-Approval Date"],
                deadline=row["Deadline"],
                application_number=row["Application Number"],
                potential_rebate=row["Potential Rebate"]
            )
        except Exception as error:
            return (error,'data',row_count) 
    return True
