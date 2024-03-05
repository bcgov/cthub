from enum import Enum

class ARCProjectTrackingColumns(Enum):
    FUNDING_CALL = "Funding Call"
    PROPONENT = "Proponent"
    REF_NUMBER = "Ref #"
    PROJECT_TITLE = "Project Title"
    PRIMARY_LOCATION = "Primary Location"
    STATUS = "Status"
    ARC_FUNDING = "ARC Funding"
    FUNDS_ISSUED = "Funds Issued"
    START_DATE = "Start Date"
    COMPLETION_DATE = "Completion Date"
    TOTAL_PROJECT_VALUE = "Total Project Value"
    ZEV_SUB_SECTOR = "ZEV Sub-Sector"
    ON_ROAD_OFF_ROAD = "On-Road/Off-Road"
    FUEL_TYPE = "Fuel Type"
    PUBLICLY_ANNOUNCED = "Publicly Announced"

class ArcProjectTrackingColumnMapping(Enum):
    funding_call = "Funding Call"
    proponent = "Proponent"
    reference_number = "Ref #"
    project_title = "Project Title"
    primary_location = "Primary Location"
    status = "Status"
    arc_funding = "ARC Funding"
    funds_issued = "Funds Issued"
    start_date = "Start Date"
    completion_date = "Completion Date"
    total_project_value = "Total Project Value"
    zev_sub_sector = "ZEV Sub-Sector"
    on_road_off_road = "On-Road/Off-Road"
    fuel_type = "Fuel Type"
    publicly_announced = "Publicly Announced"


class EVChargingRebatesColumns(Enum):
    ORGANIZATION = "Organization"
    MLA = "MLA"
    REGION = "Region"
    CITY = "City"
    ADDRESS = "Address"
    NUMBER_OF_FAST_CHARGING_STATIONS = "Number of Fast Charging Stations"
    IN_SERVICE_DATE = "In service date"
    EXPECTED_IN_SERVICE_DATE = "Expected in service date"
    ANNOUNCED = "Announced?"
    BC_EMPR_FUNDING_ANTICIPATED = "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)"
    NOTES = "Notes"

class DataFleetsColumns(Enum):
    CURRENT_STAGE = "Current Stage"
    REBATE_VALUE = "Rebate Value"
    LEGAL_NAME_OF_ORGANIZATION = "Legal Name of your Organization/Fleet: "
    BUSINESS_CATEGORY = "Your business Category"
    CITY = "City:*"
    POSTAL_CODE = "Postal Code:*"
    APPLICANT_FIRST_NAME = "Applicant First Name"
    APPLICANT_LAST_NAME = "Applicant Last Name"
    EMAIL_ADDRESS = "Email Address:*"
    FLEET_SIZE_ALL = "Fleet Size All"
    FLEET_SIZE_LIGHT_DUTY = "Fleet Size Light-duty"
    TOTAL_NUMBER_OF_EVS = "Total number of EVs?"
    TOTAL_NUMBER_OF_LIGHT_DUTY_EVS = "Total number of light-duty EVs?"
    PHEVS = "PHEV's"
    EVSES = "EVSE's?"
    AVERAGE_DAILY_TRAVEL_DISTANCE = "Average daily travel distance?"
    WHICH_COMPONENT_ARE_YOU_APPLYING_FOR = "Which component are you applying for?*"
    ESTIMATED_COST = "Estimated cost"
    WHICH_TYPE_OF_CHARGER_ARE_YOU_INSTALLING = "Which type of charger are you installing?"
    HOW_MANY_LEVEL_2_CHARGING_STATIONS = "How many Level 2 Charging Stations are you applying for"
    HOW_MANY_LEVEL_3_DC_FAST_CHARGING_STATIONS = "How many Level 3/DC Fast Charging Stations are you applying for"
    APPLICATION_FORM_FLEETS_COMPLETION_DATE_TIME = '"Application Form Fleets" completion date/time'
    PRE_APPROVAL_DATE = "Pre-Approval Date"
    DEADLINE = "Deadline"
    APPLICATION_NUMBER = "Application Number"
    POTENTIAL_REBATE = "Potential Rebate"

class HydrogenFleetsColumns(Enum):
    APPLICATION_NUMBER = "Application #"
    FLEET_NUMBER = "Fleet #"
    APPLICATION_DATE = "Application Date"
    ORGANIZATION_NAME = "Organization Name"
    FLEET_NAME = "Fleet Name"
    STREET_ADDRESS = "Street Address"
    CITY = "City"
    POSTAL_CODE = "Postal Code"
    VIN = "VIN"
    MAKE = "Make"
    MODEL = "Model"
    YEAR = "Year"
    PURCHASE_DATE = "Purchase Date"
    DEALER_NAME = "Dealer Name"
    REBATE_AMOUNT = "Rebate Amount"

class HydrogenFuelingColumns(Enum):
    STATION_NUMBER = "Station Number"
    RFP_CLOSE_DATE = "RFP Close Date"
    STATION_NAME = "Station Name"
    STREET_ADDRESS = "Street Address"
    CITY = "City"
    POSTAL_CODE = "Postal Code"
    PROPONENT = "Proponent"
    LOCATION_PARTNER = "Location Partner (Shell/7-11/etc.)"
    CAPITAL_FUNDING_AWARDED = "Capital Funding Awarded"
    OM_FUNDING_POTENTIAL = "O&M Funding Potential"
    DAILY_CAPACITY = "Daily Capacity (kg/day)"
    BAR_700 = "700 Bar"
    BAR_350 = "350 Bar"
    STATUS = "Status"
    NUMBER_OF_FUELLING_POSITIONS = "# of Fuelling Positions"
    OPERATIONAL_DATE = "Operational Date"
    OPENING_DATE = "Opening Date"
    TOTAL_CAPITAL_COST = "Total Capital Cost"

class LDVRebatesColumns(Enum):
    CASL_CONSENT = "CASL Consent"
    DATE_APPROVED = "DATE APPROVED"
    SUBMISSION_ID = "Submission ID"
    SUBMISSION_DATE = "Submission Date"
    COMPANY_NAME = "Company Name"
    CITY = "City"
    APPLICANT_NAME = "Applicant Name"
    APPLICANT_ADDRESS_1 = "Applicant Address 1"
    APPLICANT_ADDRESS_2 = "Applicant Address 2"
    APPLICANT_CITY = "Applicant City"
    APPLICANT_POSTAL_CODE = "Applicant Postal Code"
    APPLICANT_PHONE = "Applicant Phone"
    APPLICANT_EMAIL = "Applicant Email"
    APPLICANT_USE = "Applicant Use"
    APPLICANT_TYPE = "Applicant Type"
    BUSINESS_NAME = "Business Name"
    BUSINESS_NUMBER = "Business Number"
    DRIVERS_LICENSE = "Drivers License"
    PROVINCE = "Province"
    MSRP = "MSRP"
    OTHER_INCENTIVES = "Other Incentives"
    DOCUMENT_TYPE = "Document Type"
    VEHICLE = "Vehicle"
    INCENTIVE_AMOUNT = "Incentive Amount"
    VIN = "VIN#"
    DELIVERED = "Delivered"
    CONSENT_TO_CONTACT = "Consent to Contact"

class PublicChargingColumns(Enum):
    APPLICANT_NAME = "Applicant Name"
    ADDRESS = "Address"
    CHARGING_STATION_INFO = "Charging Station Info"
    GT_25KW_LT_50KW = ">25kW; <50kW"
    GT_50KW_LT_100KW = ">50kW; <100kW"
    GT_100KW = ">100kW"
    LEVEL_2_UNITS_STATIONS = "Level 2 (# of units/stations)"
    LEVEL_2_PORTS = "Level 2 (# of ports)"
    ESTIMATED_BUDGET = "Estimated Budget"
    ADJUSTED_REBATE = "Adjusted Rebate"
    REBATE_PERCENT_MAXIMUM = "Rebate % Maximum"
    PILOT_PROJECT = "Pilot Project (Y/N)"
    REGION = "Region"
    ORGANIZATION_TYPE = "Organization Type"
    PROJECT_STATUS = "Project Status"
    REVIEW_NUMBER = "Review Number"
    PAID_OUT_REBATE_AMOUNT = "Paid out rebate amount"

class ScrapItColumns(Enum):
    APPROVAL_NUM = "Approval Num"
    APP_RECVD_DATE = "App Recv'd Date"
    COMPLETION_DATE = "Completion Date"
    POSTAL_CODE = "Postal Code"
    VIN = "VIN"
    APP_CITY_FUEL = "App City Fuel"
    INCENTIVE_TYPE = "Incentive Type"
    INCENTIVE_COST = "Incentive Cost"
    CHEQUE_NUMBER = "Cheque #"
    BUDGET_CODE = "Budget Code"
    SCRAP_DATE = "Scrap Date"

class SpecialtyUseVehicleIncentiveProgramColumns(Enum):
    APPROVALS = "Approvals"
    DATE = "Date"
    APPLICANT_NAME = "Applicant Name"
    MAX_INCENTIVE_AMOUNT_REQUESTED = "Max Incentive Amount Requested"
    CATEGORY = "Category"
    FLEET = "Fleet"
    INDIVIDUAL = "Individual"
    INCENTIVE_PAID = "Incentive Paid"
    TOTAL_PURCHASE_PRICE_PRE_TAX = "Total Purchase Price (pre-tax)"
    MANUFACTURER = "Manufacturer"
    MODEL = "Model"

dataset_columns = {
    'ARC Project Tracking': ARCProjectTrackingColumns,
    'EV Charging Rebates': EVChargingRebatesColumns,
    'Data Fleets': DataFleetsColumns,
    'Hydrogen Fleets': HydrogenFleetsColumns,
    'Hydrogen Fueling': HydrogenFuelingColumns,
    'LDV Rebates': LDVRebatesColumns,
    'Public Charging': PublicChargingColumns,
    'Scrap It': ScrapItColumns,
    'Specialty Use Vehicle Incentive Program': SpecialtyUseVehicleIncentiveProgramColumns,
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