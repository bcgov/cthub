import datetime
from decimal import Decimal
from enum import Enum

from api.models.arc_project_tracking import ARCProjectTracking
from api.models.charger_rebates import ChargerRebates
from api.models.data_fleets import DataFleets
from api.models.hydrogen_fleets import HydrogenFleets
from api.models.hydrogen_fueling import HydrogrenFueling
from api.models.ldv_rebates import LdvRebates
from api.models.public_charging import PublicCharging
from api.models.scrap_it import ScrapIt
from api.models.go_electric_rebates import GoElectricRebates
from api.models.cvp_data import CVPData
from api.services.spreadsheet_uploader_prep import (
    prepare_arc_project_tracking,
    prepare_hydrogen_fleets,
    prepare_hydrogen_fueling,
    prepare_ldv_rebates,
    prepare_public_charging,
    prepare_scrap_it,
    prepare_go_electric_rebates,
    prepare_cvp_data,
    validate_phone_numbers,
    typo_checker,
    location_checker,
    email_validator,
    validate_field_values,
    region_checker,
    format_postal_codes
)
from api.services.resolvers import get_google_resolver
from api.constants.misc import GER_VALID_FIELD_VALUES, ARC_VALID_FIELD_VALUES, LOCALITY_FEATURES_MAP, CVP_DATA_VALID_FIELD_VALUES


from enum import Enum

class ARCProjectTrackingColumns(Enum):
    REFERENCE_NUMBER = "Ref #"
    PROPONENT = "Proponent"
    STATUS = "Status"
    FUNDING_CALL = "Funding Call"
    PROJECT_TITLE = "Project Title"
    VEHICLE_CATEGORY = "Vehicle Category"
    ZEV_SUB_SECTOR = "ZEV Sub-Section"
    FUEL_TYPE = "Fuel Type"
    RETROFIT = "Retrofit"
    PRIMARY_LOCATION = "Primary Location"
    ECONOMIC_REGION = "Economic Region"
    JOBS = "Jobs (FTEs)"
    FUNDS_COMMITED = "Funds Committed"
    FUNDS_DISBURSED = "Funds Disbursed"
    REMAINING_DISBURSED = "Remaining To Disburse"
    TOTAL_PROJECT_VALUE = "Total Project Value"
    START_DATE = "Start Date"
    COMPLETION_DATE = "Completion Date"
    COMPLETE_OR_TERMINATION_DATE = "Complete or Termination date"
    PUBLICLY_ANNOUNCED = "Publicly Announced"
    NOTES = "Notes"

class ArcProjectTrackingColumnMapping(Enum):
    reference_number = "Ref #"
    proponent = "Proponent"
    status = "Status"
    funding_call = "Funding Call"
    project_title = "Project Title"
    vehicle_category = "Vehicle Category"
    zev_sub_sector = "ZEV Sub-Section"
    fuel_type = "Fuel Type"
    retrofit = "Retrofit"
    primary_location = "Primary Location"
    economic_region = "Economic Region"
    jobs = "Jobs (FTEs)"
    funds_commited = "Funds Committed"
    funds_disbursed = "Funds Disbursed"
    remaining_disbursed = "Remaining To Disburse"
    total_project_value = "Total Project Value"
    start_date = "Start Date"
    completion_date = "Completion Date"
    complete_or_termination_date = "Complete or Termination date"
    publicly_announced = "Publicly Announced"
    notes = "Notes"

class EVChargingRebatesColumns(Enum):
    ORGANIZATION = "Organization"
    REGION = "Region"
    CITY = "City"
    ADDRESS = "Address"
    NUMBER_OF_FAST_CHARGING_STATIONS = "Number of Fast Charging Stations"
    IN_SERVICE_DATE = "In service date"
    EXPECTED_IN_SERVICE_DATE = "Expected in service date"
    ANNOUNCED = "Announced?"
    BC_EMPR_FUNDING_ANTICIPATED = "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)"
    NOTES = "Notes"


class EVChargingRebatesColumnMapping(Enum):
    organization = "Organization"
    region = "Region"
    city = "City"
    address = "Address"
    number_of_fast_charging_stations = "Number of Fast Charging Stations"
    in_service_date = "In service date"
    expected_in_service_date = "Expected in service date"
    announced = "Announced?"
    rebate_paid = "B.C. (EMPR) Funding Anticipated (Max $25,000 per station, excludes MOTI stations) (Not all funding paid out yet as depends on station completion)"
    notes = "Notes"


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
    WHICH_TYPE_OF_CHARGER_ARE_YOU_INSTALLING = (
        "Which type of charger are you installing?"
    )
    HOW_MANY_LEVEL_2_CHARGING_STATIONS = (
        "How many Level 2 Charging Stations are you applying for"
    )
    HOW_MANY_LEVEL_3_DC_FAST_CHARGING_STATIONS = (
        "How many Level 3/DC Fast Charging Stations are you applying for"
    )
    APPLICATION_FORM_FLEETS_COMPLETION_DATE_TIME = (
        '"Application Form Fleets" completion date/time'
    )
    PRE_APPROVAL_DATE = "Pre-Approval Date"
    DEADLINE = "Deadline"
    APPLICATION_NUMBER = "Application Number"
    POTENTIAL_REBATE = "Potential Rebate"


class DataFleetsColumnMapping(Enum):
    current_stage = "Current Stage"
    rebate_value = "Rebate Value"
    legal_name_of_organization_fleet = "Legal Name of your Organization/Fleet: "
    business_category = "Your business Category"
    city = "City:*"
    postal_code = "Postal Code:*"
    applicant_first_name = "Applicant First Name"
    applicant_last_name = "Applicant Last Name"
    email_address = "Email Address:*"
    fleet_size_all = "Fleet Size All"
    fleet_size_light_duty = "Fleet Size Light-duty"
    total_number_of_evs = "Total number of EVs?"
    total_number_of_light_duty_evs = "Total number of light-duty EVs?"
    phev = "PHEV's"
    evse = "EVSE's?"
    average_daily_travel_distance = "Average daily travel distance?"
    component_being_applied_for = "Which component are you applying for?*"
    estimated_cost = "Estimated cost"
    type_of_charger_being_installed = "Which type of charger are you installing?"
    number_of_level_2_charging_stations_being_applied_for = (
        "How many Level 2 Charging Stations are you applying for"
    )
    number_of_level_3_dc_fast_charging_stations_being_applied_for = (
        "How many Level 3/DC Fast Charging Stations are you applying for"
    )
    application_form_fleets_completion_date_time = (
        '"Application Form Fleets" completion date/time'
    )
    pre_approval_date = "Pre-Approval Date"
    deadline = "Deadline"
    application_number = "Application Number"
    potential_rebate = "Potential Rebate"


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


class HydrogenFleetsColumnMapping(Enum):
    application_number = "Application #"
    fleet_number = "Fleet #"
    application_date = "Application Date"
    organization_name = "Organization Name"
    fleet_name = "Fleet Name"
    street_address = "Street Address"
    city = "City"
    postal_code = "Postal Code"
    vin = "VIN"
    make = "Make"
    model = "Model"
    year = "Year"
    purchase_date = "Purchase Date"
    dealer_name = "Dealer Name"
    rebate_amount = "Rebate Amount"


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
    OPERATIONAL_DATE = "Operational Date "
    OPENING_DATE = "Opening Date"
    TOTAL_CAPITAL_COST = "Total Capital Cost"


class HydrogenFuelingColumnMapping(Enum):
    station_number = "Station Number"
    rfp_close_date = "RFP Close Date"
    station_name = "Station Name"
    street_address = "Street Address"
    city = "City"
    postal_code = "Postal Code"
    proponent = "Proponent"
    location_partner = "Location Partner (Shell/7-11/etc.)"
    capital_funding_awarded = "Capital Funding Awarded"
    om_funding_potential = "O&M Funding Potential"
    daily_capacity = "Daily Capacity (kg/day)"
    bar_700 = "700 Bar"
    bar_350 = "350 Bar"
    status = "Status"
    number_of_fueling_positions = "# of Fuelling Positions"
    operational_date = "Operational Date "
    opening_date = "Opening Date"
    total_capital_cost = "Total Capital Cost"


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


class LdvRebatesColumnMapping(Enum):
    casl_consent = "CASL Consent"
    date_approved = "DATE APPROVED"
    submission_id = "Submission ID"
    submission_date = "Submission Date"
    company_name = "Company Name"
    city = "City"
    applicant_name = "Applicant Name"
    applicant_address_1 = "Applicant Address 1"
    applicant_address_2 = "Applicant Address 2"
    applicant_city = "Applicant City"
    applicant_postal_code = "Applicant Postal Code"
    applicant_phone = "Applicant Phone"
    applicant_email = "Applicant Email"
    applicant_use = "Applicant Use"
    applicant_type = "Applicant Type"
    business_name = "Business Name"
    business_number = "Business Number"
    drivers_license = "Drivers License"
    province = "Province"
    msrp = "MSRP"
    other_incentives = "Other Incentives"
    document_type = "Document Type"
    vehicle = "Vehicle"
    incentive_amount = "Incentive Amount"
    vin = "VIN#"
    delivered = "Delivered"
    consent_to_contact = "Consent to Contact"


class PublicChargingColumns(Enum):
    APPLICANT_NAME = "Applicant Name"
    ADDRESS = "Address"
    CHARGING_STATION_INFO = "Charging Station Info"
    GT_25KW_LT_50KW = ">25kW; <50kW"
    GT_50KW_LT_100KW = ">50kW; <100kW"
    GT_100KW = ">100kW "
    LEVEL_2_UNITS_STATIONS = "Level 2 (# of units/stations)"
    LEVEL_2_PORTS = "Level 2 (# of ports)"
    ESTIMATED_BUDGET = "Estimated Budget"
    ADJUSTED_REBATE = "Adjusted Rebate "
    REBATE_PERCENT_MAXIMUM = "Rebate % Maximum "
    PILOT_PROJECT = "Pilot Project (Y/N)"
    REGION = "Region"
    ORGANIZATION_TYPE = "Organization Type"
    PROJECT_STATUS = "Project Status"
    REVIEW_NUMBER = "Review Number"
    PAID_OUT_REBATE_AMOUNT = "Paid out rebate amount"


class PublicChargingColumnMapping(Enum):
    applicant_name = "Applicant Name"
    address = "Address"
    charging_station_info = "Charging Station Info"
    between_25kw_and_50kw = ">25kW; <50kW"
    between_50kw_and_100kw = ">50kW; <100kW"
    over_100kw = ">100kW "
    level_2_units = "Level 2 (# of units/stations)"
    level_2_ports = "Level 2 (# of ports)"
    estimated_budget = "Estimated Budget"
    adjusted_rebate = "Adjusted Rebate "
    rebate_percent_maximum = "Rebate % Maximum "
    pilot_project = "Pilot Project (Y/N)"
    region = "Region"
    organization_type = "Organization Type"
    project_status = "Project Status"
    review_number = "Review Number"
    rebate_paid = "Paid out rebate amount"


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


class ScrapItColumnMapping(Enum):
    approval_number = "Approval Num"
    application_received_date = "App Recv'd Date"
    completion_date = "Completion Date"
    postal_code = "Postal Code"
    vin = "VIN"
    application_city_fuel = "App City Fuel"
    incentive_type = "Incentive Type"
    incentive_cost = "Incentive Cost"
    cheque_number = "Cheque #"
    budget_code = "Budget Code"
    scrap_date = "Scrap Date"


class GoElectricRebatesColumns(Enum):
    APPROVALS = "Approvals"
    DATE = "Date"
    APPLICANT_NAME = "Applicant Name"
    MAX_INCENTIVE_AMOUNT_REQUESTED = "Max Incentive Amount Requested"
    CATEGORY = "Category"
    APPLICANT_TYPE = "Fleet/Individuals"
    INCENTIVE_PAID = "Incentive Paid"
    TOTAL_PURCHASE_PRICE_PRE_TAX = "Total Purchase Price (pre-tax)"
    MANUFACTURER = "Manufacturer"
    MODEL = "Model"
    CITY = "City"
    POSTAL_CODE = "Postal code"
    PHONE = "Phone Number"
    EMAIL = "Email"
    VIN = "VIN Number"
    VEHICLE_CLASS = "Class"
    REBATE_ADJUSTMENT = "Rebate adjustment (discount)"
    NOTES = "Notes"


class GoElectricRebatesColumnMapping(Enum):
    approvals = "Approvals"
    date = "Date"
    applicant_name = "Applicant Name"
    max_incentive_amount_requested = "Max Incentive Amount Requested"
    category = "Category"
    applicant_type = "Fleet/Individuals"
    incentive_paid = "Incentive Paid"
    total_purchase_price = "Total Purchase Price (pre-tax)"
    manufacturer = "Manufacturer"
    model = "Model"
    city = "City"
    postal_code = "Postal code"
    phone = "Phone Number"
    email = "Email"
    vin = "VIN Number"
    vehicle_class = "Class"
    rebate_adjustment = "Rebate adjustment (discount)"
    notes = "Notes"

class CVPDataColumns(Enum):
    FUNDING_CALL = "FC"
    PROJECT_IDENTIFIER = "Project Identifier"
    APPLICANT_NAME = "Name of Applicant"
    RANK = "Rank"
    STATUS = "Status"
    SCORE = "Score"
    VEHICLE_DEPLOYED = "Vehicle Deployed"
    VEHICLE_CATEGORY = "Vehicle Category"
    DRIVE_TYPE = "Drive Type"
    VEHICLE_TYPE = "Vehicle Type"
    ROAD_CLASS = "Class"
    USE_CASE = "Use Case"
    MAKE_AND_MODEL = "Vehicle Make and Model"
    ECONOMIC_REGION = "Economic Region"
    START_DATE = "Start Date"
    COMPLETION_DATE = "Completion Date"
    PROJECT_TYPE = "Project Type"
    CLASS_3 = "Class 3"
    CLASS_4 = "Class 4"
    CLASS_5 = "Class 5"
    CLASS_6 = "Class 6"
    CLASS_7 = "Class 7"
    CLASS_8 = "Class 8"
    ON_ROAD_TOTAL = "On Road Total"
    OFF_ROAD = "Off-Road"
    LEVEL_2_CHARGER = "Level 2 Charger (3.3 kW to 19.2 kW)"
    LEVEL_3_CHARGER = "Level 3 Charger (20 kW to 49 kW)"
    HIGH_LEVEL_3_CHARGER = "Level 3 Charger (50 kW to 99kW)"
    LEVEL_CHARGER = "Level Charger (100 kW and above)"
    OTHER_CHARGER = "Other Charger"
    H2_FUELING_STATION = "H2 Fueling Station"
    CHARGER_BRAND = "Charger Brand"
    H2_FUELLING_STATION_DESCRIPTION = "H2 Fuelling Station Description"
    GHG_EMISSION_REDUCTION = "Proponent's GHG Emission Reduction (tCO2e/yr)"
    ESTIMATED_GHG_EMISSION_REDUCTION = "Le-ef Estimated GHG Reduction (tCO2e/yr)"
    FUNDING_EFFICIENCY = "Funding Efficiency for Emmision Abatment ($/tCO2e)"
    MARKET_EMISSION_REDUCTIONS = "Market Emission Reductions (tCO2e by 2030)"
    CVP_FUNDING_REQUEST = "CVP Program Funding Request (Initial)"
    CVP_FUNDING_CONTRIBUTION = "CVP Funding (approved - Contribution Agreement)"
    EXTERNAL_FUNDING = "External Funding"
    PROPONENT_FUNDING = "Proponent funding"
    PROJECT_COST_INITIAL = "Total project cost (initial)"
    PROJECT_COST_REVISED = "Total Project Cost (revised)"
    FUNDING_SOURCE = "Funding Source"
    NOTES = "Notes"
    IMHZEV = "iMHZEV"

class CVPDataColumnMapping(Enum):
    funding_call = "FC"
    project_identifier = "Project Identifier"
    applicant_name = "Name of Applicant"
    rank = "Rank"
    status = "Status"
    score = "Score"
    vehicle_deployed = "Vehicle Deployed"
    vehicle_category = "Vehicle Category"
    drive_type = "Drive Type"
    vehicle_type = "Vehicle Type"
    road_class = "Class"
    use_case = "Use Case"
    make_and_model = "Vehicle Make and Model"
    economic_region = "Economic Region"
    start_date = "Start Date"
    completion_date = "Completion Date"
    project_type = "Project Type"
    class_3 = "Class 3"
    class_4 = "Class 4"
    class_5 = "Class 5"
    class_6 = "Class 6"
    class_7 = "Class 7"
    class_8 = "Class 8"
    on_road_total = "On Road Total"
    off_road = "Off-Road"
    level_2_charger = "Level 2 Charger (3.3 kW to 19.2 kW)"
    level_3_charger = "Level 3 Charger (20 kW to 49 kW)"
    high_level_3_charger = "Level 3 Charger (50 kW to 99kW)"
    level_charger = "Level Charger (100 kW and above)"
    other_charger = "Other Charger"
    h2_fuelling_station = "H2 Fueling Station"
    charger_brand = "Charger Brand"
    h2_fuelling_station_description = "H2 Fuelling Station Description"
    ghg_emission_reduction = "Proponent's GHG Emission Reduction (tCO2e/yr)"
    estimated_ghg_emission_reduction = "Le-ef Estimated GHG Reduction (tCO2e/yr)"
    funding_efficiency = "Funding Efficiency for Emmision Abatment ($/tCO2e)"
    market_emission_reductions = "Market Emission Reductions (tCO2e by 2030)"
    cvp_funding_request = "CVP Program Funding Request (Initial)"
    cvp_funding_contribution = "CVP Funding (approved - Contribution Agreement)"
    external_funding = "External Funding"
    proponent_funding = "Proponent funding"
    project_cost_initial = "Total project cost (initial)"
    project_cost_revised = "Total Project Cost (revised)"
    funding_source = "Funding Source"
    notes = "Notes"
    imhzev = "iMHZEV"


FIELD_TYPES = {
    "ARC Project Tracking": {
        "reference_number": str,
        "proponent": str,
        "status": str,
        "funding_call": str,
        "project_title": str,
        "vehicle_category": str,
        "zev_sub_sector": str,
        "fuel_type": str,
        "retrofit": str,
        "primary_location": str,
        "economic_region": str,
        "jobs": int,
        "funds_commited": int,
        "funds_disbursed": int,
        "remaining_disbursed": int,
        "total_project_value": int,
        "start_date": datetime.date,
        "completion_date": datetime.date,
        "complete_or_termination_date": datetime.date,
        "publicly_announced": str,
        "notes": str,
    },
    "EV Charging Rebates": {
        "organization": str,
        "region": str,
        "city": str,
        "address": str,
        "number_of_fast_charging_stations": int,
        "in_service_date": str,
        "expected_in_service_date": str,
        "announced": str,
        "rebate_paid": float,
        "notes": str,
    },
    "Data Fleets": {
        "current_stage": str,
        "rebate_value": str,
        "legal_name_of_organization_fleet": str,
        "business_category": str,
        "city": str,
        "postal_code": str,
        "applicant_first_name": str,
        "applicant_last_name": str,
        "email_address": str,
        "fleet_size_all": int,
        "fleet_size_light_duty": int,
        "total_number_of_evs": int,
        "total_number_of_light_duty_evs": int,
        "phev": int,
        "evse": int,
        "average_daily_travel_distance": str,
        "component_being_applied_for": str,
        "estimated_cost": str,
        "type_of_charger_being_installed": str,
        "number_of_level_2_charging_stations_being_applied_for": int,
        "number_of_level_3_dc_fast_charging_stations_being_applied_for": int,
        "application_form_fleets_completion_date_time": str,
        "pre_approval_date": str,
        "deadline": str,
        "application_number": str,
        "potential_rebate": str,
    },
    "Hydrogen Fleets": {
        "application_number": int,
        "fleet_number": int,
        "application_date": str,
        "organization_name": str,
        "fleet_name": str,
        "street_address": str,
        "city": str,
        "postal_code": str,
        "vin": str,
        "make": str,
        "model": str,
        "year": str,
        "purchase_date": str,
        "dealer_name": str,
        "rebate_amount": str,
    },
    "Hydrogen Fueling": {
        "station_number": int,
        "rfp_close_date": datetime.date,
        "station_name": str,
        "street_address": str,
        "city": str,
        "postal_code": str,
        "proponent": str,
        "location_partner": str,
        "capital_funding_awarded": Decimal,
        "om_funding_potential": Decimal,
        "daily_capacity": int,
        "bar_700": bool,
        "bar_350": bool,
        "status": str,
        "number_of_fueling_positions": int,
        "operational_date": datetime.date,
        "opening_date": datetime.date,
        "total_capital_cost": Decimal,
    },
    "LDV Rebates": {
        "casl_consent": bool,
        "date_approved": str,
        "submission_id": int,
        "submission_date": str,
        "company_name": str,
        "city": str,
        "applicant_name": str,
        "applicant_address_1": str,
        "applicant_address_2": str,
        "applicant_city": str,
        "applicant_postal_code": str,
        "applicant_phone": str,
        "applicant_email": str,
        "applicant_use": str,
        "applicant_type": str,
        "business_name": str,
        "business_number": str,
        "drivers_license": str,
        "province": str,
        "msrp": Decimal,
        "other_incentives": str,
        "document_type": str,
        "vehicle": str,
        "incentive_amount": Decimal,
        "vin": str,
        "delivered": bool,
        "consent_to_contact": bool,
    },
    "Public Charging": {
        "applicant_name": str,
        "address": str,
        "charging_station_info": str,
        "between_25kw_and_50kw": int,
        "between_50kw_and_100kw": int,
        "over_100kw": int,
        "level_2_units": int,
        "level_2_ports": int,
        "estimated_budget": float,
        "adjusted_rebate": float,
        "rebate_percent_maximum": float,
        "pilot_project": bool,
        "region": str,
        "organization_type": str,
        "project_status": str,
        "review_number": int,
        "rebate_paid": float,
    },
    "Scrap It": {
        "approval_number": int,
        "application_received_date": str,
        "completion_date": str,
        "postal_code": str,
        "vin": str,
        "application_city_fuel": Decimal,
        "incentive_type": str,
        "incentive_cost": Decimal,
        "cheque_number": str,
        "budget_code": str,
        "scrap_date": str,
    },
    "Go Electric Rebates Program": {
        "approvals": str,
        "date": datetime.date,
        "applicant_name": str,
        "max_incentive_amount_requested": int,
        "category": str,
        "applicant_type": str,
        "incentive_paid": int,
        "total_purchase_price": int,
        "manufacturer": str,
        "model": str,
        "city": str,
        "postal_code": str,
        "phone": str,
        "email": str,
        "vin": str,
        "vehicle_class": str,
        "rebate_adjustment": str,
        "notes": str,
    },
    "CVP Data": {
        "funding_call": int,
        "project_identifier": int,
        "applicant_name": str,
        "rank": int,
        "status": str,
        "score": int,
        "vehicle_deployed": str,
        "vehicle_category": str,
        "drive_type": str,
        "vehicle_type": str,
        "road_class": str,
        "use_case": str,
        "make_and_model": str,
        "economic_region": str,
        "start_date": datetime.date,
        "completion_date": datetime.date,
        "project_type": str,
        "class_3": int,
        "class_4": int,
        "class_5": int,
        "class_6": int,
        "class_7": int,
        "class_8": int,
        "on_road_total": int,
        "off_road": int,
        "level_2_charger": int,
        "level_3_charger": int,
        "high_level_3_charger": int,
        "level_charger": int,
        "other_charger": int,
        "h2_fuelling_station": int,
        "charger_brand": str,
        "h2_fuelling_station_description": str,
        "ghg_emission_reduction": int,
        "estimated_ghg_emission_reduction": int,
        "funding_efficiency": int,
        "market_emission_reductions": int,
        "cvp_funding_request": int,
        "cvp_funding_contribution": int,
        "external_funding": int,
        "proponent_funding": int,
        "project_cost_initial": int,
        "project_cost_revised": int,
        "funding_source": str,
        "notes": str,
        "imhzev": str,
    },


}

DATASET_CONFIG = {
    "ARC Project Tracking": {
        "model": ARCProjectTracking,
        "columns": ARCProjectTrackingColumns,
        "column_mapping": ArcProjectTrackingColumnMapping,
        "sheet_name": "ARC Data",
        "preparation_functions": [prepare_arc_project_tracking],
        "validation_functions": [
            {'function': validate_field_values, "columns": [], "kwargs": {"indices_offset":2, "fields_and_values": ARC_VALID_FIELD_VALUES}},
            {"function": region_checker, "columns": ['Economic Region'], "kwargs": {"indices_offset":2}},
        ]
    },
    "EV Charging Rebates": {
        "model": ChargerRebates,
        "columns": EVChargingRebatesColumns,
        "column_mapping": EVChargingRebatesColumnMapping,
        "sheet_name": "Updated",
        "header_row": 2,
    },
    "Data Fleets": {
        "model": DataFleets,
        "columns": DataFleetsColumns,
        "column_mapping": DataFleetsColumnMapping,
        "sheet_name": "Data Fleets",
    },
    "Hydrogen Fleets": {
        "model": HydrogenFleets,
        "columns": HydrogenFleetsColumnMapping,
        "column_mapping": HydrogenFleetsColumnMapping,
        "sheet_name": "Fleets",
        "preparation_functions": [prepare_hydrogen_fleets],
    },
    "Hydrogen Fueling": {
        "model": HydrogrenFueling,
        "columns": HydrogenFuelingColumnMapping,
        "column_mapping": HydrogenFuelingColumnMapping,
        "sheet_name": "Station_Tracking",
        "preparation_functions": [prepare_hydrogen_fueling],
    },
    "LDV Rebates": {
        "model": LdvRebates,
        "columns": LdvRebatesColumnMapping,
        "sheet_name": "Raw Data",
        "preparation_functions": [prepare_ldv_rebates],
    },
    "Public Charging": {
        "model": PublicCharging,
        "columns": PublicChargingColumns,
        "column_mapping": PublicChargingColumnMapping,
        "sheet_name": "Project_applications",
        "header_row": 2,
        "preparation_functions": [prepare_public_charging],
    },
    "Scrap It": {
        "model": ScrapIt,
        "columns": ScrapItColumns,
        "column_mapping": ScrapItColumnMapping,
        "sheet_name": "TOP OTHER TRANSACTIONS",
        "header_row": 5,
        "preparation_functions": [prepare_scrap_it],
    },
    "Go Electric Rebates Program": {
        "model": GoElectricRebates,
        "columns": GoElectricRebatesColumns,
        "column_mapping": GoElectricRebatesColumnMapping,
        "sheet_name": "Distribution List - Master",
        "preparation_functions": [prepare_go_electric_rebates],
        "validation_functions": [
            {"function": validate_phone_numbers, "columns": ["Phone Number"], "kwargs": {"indices_offset": 2}},
            {"function": typo_checker, "columns": ["Applicant Name"], "kwargs": {"cutoff": 0.8, "indices_offset": 2}},
            {"function": location_checker, "columns": ["City"], "kwargs": {"columns_to_features_map": {"City": LOCALITY_FEATURES_MAP}, "indices_offset":2}},
            {"function": email_validator, "columns": ["Email"], "kwargs": {"indices_offset":2, "get_resolver": get_google_resolver}},
            {"function": validate_field_values, "columns": [], "kwargs": {"indices_offset":2, "fields_and_values": GER_VALID_FIELD_VALUES}},
            {"function": format_postal_codes, "columns": ["Postal code"], "kwargs": {"indices_offset":2, "validate": True}}
        ]
    },
    "CVP Data": {
        "model": CVPData,
        "columns": CVPDataColumns,
        "column_mapping": CVPDataColumnMapping,
        "sheet_name": "Data",
        "preparation_functions": [prepare_cvp_data],
        "validation_functions": [{"function": validate_field_values, "columns": [], "kwargs": {"indices_offset":2, "fields_and_values": CVP_DATA_VALID_FIELD_VALUES, "delimiter": ","}},]
    },

}
