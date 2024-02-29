import pandas as pd
from io import BytesIO
from api.services.spreadsheet_uploader_prep import DATASET_COLUMNS

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
