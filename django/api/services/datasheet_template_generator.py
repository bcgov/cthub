import pandas as pd
from io import BytesIO

DATASET_COLUMNS = {
    'ARC Project Tracking': [
        "Funding Call", "Proponent", "Ref #", "Project Title", "Primary Location",
        "Status", "ARC Funding", "Funds Issued", "Start Date", "Completion Date",
        "Total Project Value", "ZEV Sub-Sector", "On-Road/Off-Road", "Fuel Type",
        "Publicly Announced",
    ],
    # Charger Rebates
    'EV Charging Rebates': [
        "Organization", "MLA", "Region", "City",
        "Address", "Number of Fast Charging Stations", "In service date",
        "Expected in service date", "Announced?",
        "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)",
        "Notes",
    ],
    'Data Fleets': [
        "Current Stage", "Rebate Value", "Legal Name of your Organization/Fleet: ",
        "Your business Category", "City:*", "Postal Code:*", "Applicant First Name",
        "Applicant Last Name", "Email Address:*", "Fleet Size All",
        "Fleet Size Light-duty", "Total number of EVs?", "Total number of light-duty EVs?",
        "PHEV's", "EVSE's?", "Average daily travel distance?", "Which component are you applying for?*",
        "Estimated cost", "Which type of charger are you installing?",
        "How many Level 2 Charging Stations are you applying for",
        "How many Level 3/DC Fast Charging Stations are you applying for",
        '"Application Form Fleets" completion date/time',
        "Pre-Approval Date", "Deadline", "Application Number", "Potential Rebate"
    ],
    # Hydrogen Fleets
    'Hydrogen Fleets': [
        "Application #",
        "Fleet #",
        "Application Date",
        "Organization Name",
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
    ],
    # Hydrogen Fueling
    'Hydrogen Fueling': [
        "Station Number",
        "RFP Close Date",
        "Station Name",
        "Street Address",
        "City",
        "Postal Code",
        "Proponent",
        "Location Partner (Shell/7-11/etc.)",
        "Capital Funding Awarded",
        "O&M Funding Potential",
        "Daily Capacity (kg/day)",
        "700 Bar",
        "350 Bar",
        "Status",
        "# of Fuelling Positions",
        "Operational Date",
        "Opening Date",
        "Total Capital Cost",
    ],
    # LDV Rebates
    'LDV Rebates': [
        "CASL Consent",
        "DATE APPROVED",
        "Submission ID",
        "Submission Date",
        "Company Name",
        "City",
        "Applicant Name",
        "Applicant Address 1",
        "Applicant Address 2",
        "Applicant City",
        "Applicant Postal Code",
        "Applicant Phone",
        "Applicant Email",
        "Applicant Use",
        "Applicant Type",
        "Business Name",
        "Business Number",
        "Drivers License",
        "Province",
        "MSRP",
        "Other Incentives",
        "Document Type",
        "Vehicle",
        "Incentive Amount",
        "VIN#",
        "Delivered",
        "Consent to Contact"
    ],
    # Public Charging
    'Public Charging': [
        "Applicant Name",
        "Address",
        "Charging Station Info",
        ">25kW; <50kW",
        ">50kW; <100kW",
        ">100kW",
        "Level 2 (# of units/stations)",
        "Level 2 (# of ports)",
        "Estimated Budget",
        "Adjusted Rebate",
        "Rebate % Maximum",
        "Pilot Project (Y/N)",
        "Region",
        "Organization Type",
        "Project Status",
        "Review Number",
        "Paid out rebate amount"
    ],
    # Scrap It
    'Scrap It': [
        "Approval Num",
        "App Recv'd Date",
        "Completion Date",
        "Postal Code",
        "VIN",
        "App City Fuel",
        "Incentive Type",
        "Incentive Cost",
        "Cheque #",
        "Budget Code",
        "Scrap Date"
    ],
    # Specialty Use Vehicle Incetives
    'Specialty Use Vehicle Incentive Program': [
        "Approvals",
        "Date",
        "Applicant Name",
        "Max Incentive Amount Requested",
        "Category",
        "Fleet",
        "Individual",
        "Incentive Paid",
        "Total Purchase Price (pre-tax)",
        "Manufacturer",
        "Model",
    ],

    
}

def generate_template(dataset_name):
    """
    Generates an Excel spreadsheet template for a specified dataset.
    """
    if dataset_name not in DATASET_COLUMNS:
        raise ValueError(f"Dataset '{dataset_name}' is not supported.")

    columns = DATASET_COLUMNS[dataset_name]
    df = pd.DataFrame(columns=columns)

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        sheet_name = dataset_name
        start_row = 0
        if dataset_name == 'ARC Project Tracking':
            sheet_name = 'Project_Tracking'

        if dataset_name == 'Specialty Use Vehicle Incentive Program':
            sheet_name= 'Sheet1'

        if dataset_name == 'Public Charging':
            sheet_name= 'Project_applications'
            start_row = 2

        if dataset_name == 'LDV Rebates':
            sheet_name='Raw Data'

        if dataset_name == 'EV Charging Rebates':
            sheet_name = 'Updated'
            start_row = 2

        if dataset_name == 'Hydrogen Fueling':
            sheet_name = 'Station_Tracking'

        if dataset_name == 'Hydrogen Fleets':
            sheet_name = 'Fleets'

        if dataset_name == 'Scrap It':
            sheet_name = 'TOP OTHER TRANSACTIONS'
            start_row = 5

        df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)

    excel_buffer.seek(0)
    return excel_buffer
