import pandas as pd
from io import BytesIO
from api.constants import *

def generate_template(dataset_name):
    """
    Generates an Excel spreadsheet template for a specified dataset.
    """
    dataset_column_enum_map = {
        'ARC Project Tracking': ARCProjectTrackingColumns,
        'EV Charging Rebates': EVChargingRebatesColumns,
        'Data Fleets': DataFleetsColumns,
        'Hydrogen Fleets': HydrogenFleetsColumns,
        'Hydrogen Fueling': HydrogenFuelingColumns,
        'LDV Rebates': LDVRebatesColumns,
        'Public Charging': PublicChargingColumns,
        'Scrap It': ScrapItColumns,
        'Specialty Use Vehicle Incentive Program': SpecialityUseVehicleIncentiveProgramColumns,
    }

    if dataset_name not in dataset_column_enum_map:
        raise ValueError(f"Dataset '{dataset_name}' is not supported.")

    columns = [column.value for column in dataset_column_enum_map[dataset_name]]

    df = pd.DataFrame(columns=columns)

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        sheet_name = dataset_name.replace(" ", "_")
        start_row = 0

        custom_sheet_names = {
            'ARC Project Tracking': 'Project_Tracking',
            'Specialty Use Vehicle Incentive Program': 'Sheet1',
            'Public Charging': 'Project_applications',
            'LDV Rebates': 'Raw Data',
            'EV Charging Rebates': 'Updated',
            'Hydrogen Fueling': 'Station_Tracking',
            'Hydrogen Fleets': 'Fleets',
            'Scrap It': 'TOP OTHER TRANSACTIONS',
        }
        custom_start_rows = {
            'Public Charging': 2,
            'EV Charging Rebates': 2,
            'Scrap It': 5,
        }

        sheet_name = custom_sheet_names.get(dataset_name, sheet_name)
        start_row = custom_start_rows.get(dataset_name, start_row)

        df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)

    excel_buffer.seek(0)
    return excel_buffer