def prepare_arc_project_tracking(df):
    df['Publicly Announced'] = df['Publicly Announced'].replace({'No': False, 'N': False, 'Yes': True, 'Y': True})
    return df

COLUMN_MAPPING = {
    'ARC Project Tracking': {
        "Funding Call": "funding_call",
        "Proponent": "proponent",
        "Ref #": "reference_number",
        "Project Title": "project_title",
        "Primary Location": "primary_location",
        "Status": "status",
        "ARC Funding": "arc_funding",
        "Funds Issued": "funds_issued",
        "Start Date": "start_date",
        "Completion Date": "completion_date",
        "Total Project Value": "total_project_value",
        "ZEV Sub-Sector": "zev_sub_sector",
        "On-Road/Off-Road": "on_road_off_road",
        "Fuel Type": "fuel_type",
        "Publicly Announced": "publicly_announced",
    }
}

FIELD_TYPES = {
    'ARC Project Tracking': {
        "funding_call": str,
        "proponent": str,
        "reference_number": str,
        "project_title": str,
        "primary_location": str,
        "status": str,
        "arc_funding": int,
        "funds_issued": int,
        "start_date": str,
        "completion_date": str,
        "total_project_value": int,
        "zev_sub_sector": str,
        "on_road_off_road": str,
        "fuel_type": str,
        "publicly_announced": bool,
    }
}


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
    ]
}
