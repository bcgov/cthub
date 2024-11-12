AREA_CODES = [
    587,
    368,
    403,
    825,
    780,
    236,
    672,
    604,
    778,
    250,
    584,
    431,
    204,
    506,
    709,
    867,
    782,
    902,
    867,
    365,
    226,
    647,
    519,
    289,
    742,
    807,
    548,
    753,
    249,
    683,
    437,
    905,
    343,
    613,
    705,
    416,
    782,
    902,
    450,
    418,
    873,
    468,
    367,
    819,
    579,
    581,
    438,
    354,
    514,
    263,
    306,
    474,
    639,
    867,
]

# map of feature category codes to feature types for locality features:
LOCALITY_FEATURES_MAP = {
    1: ["City", "District Municipality (1)", "Resort Municipality", "Village (1)", "Town"],
    2: ["Community", "First Nation Village", "Former Locality", "Locality", "Recreational Community"],
    3: ["Urban Community"],
    5: ["Indian Government District", "Indian Government District : Land Unit"],
    6: ["Indian Reserve-Réserve indienne", "Region", "Regional District"],
    28: ["Canadian Forces Base", "Canadian Forces Station", "Recreation Facility"],
}

GER_VALID_FIELD_VALUES = {
    'Approvals': ['Approved', 'Approved Fraudulent'],
    'Category': [
        'Forklift', 'Low Speed', 'Motorcycle', 'Medium & Heavy Duty', 
        'Airport & Port Specialty Vehicle', 'Cargo E-Bike', 'Utility Vehicle'
    ],
    'Fleet/Individuals': ['Fleet', 'Individual'],
    'Rebate adjustment (discount)': ['Yes'],
    'Class': ['2B', '3', '4', '5', '6', '7', '8']
    }

ARC_VALID_FIELD_VALUES = {
    'Funding Call': ['ARC-2018-1', 'ARC-2020-2'],
    'Status': ['Approved', 'Completed', 'Terminated'],
    'Vehicle Category': ['On-Road', 'On/Off Road', 'Marine', 'Aviation', 'Off-Road'],
    'Zev Sub-Section': [
        'Testing and certification services', 'Battery components',
        'Vehicle components', 'Fuelling Infrastructure', 'Vehicles',
        'Transferable Technologies'
        ],
    'Fuel Type': ['H2', 'Electric'],
    'Retrofit': ['BEV Retrofit', 'Hybrid Retrofit', 'H2 Retrofit', 'N/A']
}

CVP_DATA_VALID_FIELD_VALUES = {
    'Funding Call': ['1', '2', '3', '4', '5', '6', '7', '8', '10'],
    'Status': ['Approved', 'Completed', 'Terminated', 'Not Approved', 'Application Withdrawn'],
    'Vehicles Deployed': ['Yes', 'No'],
    'Vehicle Category': ['On-Road', 'Off-Road', 'Marine', 'Rail', 'Aviation'],
    'Class': [
        'Road - 3', 'Road - 4', 'Road - 5', 'Road - 6', 'Road - 7',
        'Road - 8', 'Road - 8C'
    ],
    'Economic Region': [
        'Nechako', 'Northeast', 'North Coast', 'Cariboo', 'Vancouver Island/Coast',
        'Mainland/Southwest', 'Thompson/Okanagan', 'Kootenay', 'Across BC'
    ],
    'Drive Type': ['BEV', 'FC', 'PHEV'],
    'Vehicle Type': [
        'On-Road', 'Loader', 'Excavator', 'Forklift', 'Outboard Motor',
        'Tugboat', 'Passenger Ferry', 'Ice Resurfacer', 'Locomotive',
        'Rail Maintenance', 'Rubber-tired Gantry Crane', 'Terminal/Yard truck',
        'Aircraft', 'Jet Fuel Pumper', 'Train Mover'
    ],
    'Project Type': [
        'Procurement', 'New Design', 'Hybrid Retrofit', 'BEV Retrofit', 'H2 Retrofit'
    ]
}
