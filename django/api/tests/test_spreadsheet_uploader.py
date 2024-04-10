import io
from decimal import Decimal
from django.test import TestCase
import pandas as pd
from api.models.scrap_it import ScrapIt
from api.services.spreadsheet_uploader import import_from_xls
from api.constants import ScrapItColumnMapping, ScrapItColumns
from api.services.spreadsheet_uploader_prep import prepare_scrap_it

class UploadTests(TestCase):
    def setUp(self):

        self.field_types = {
            'approval_number': int,
            'application_received_date': str,
            'completion_date': str,
            'postal_code': str,
            'vin': str,
            'application_city_fuel': Decimal,
            'incentive_type': str,
            'incentive_cost': Decimal,
            'cheque_number': str,
            'budget_code': str,
            'scrap_date': str
        }

    def test_wrong_cell_types(self):
        data = {
            'approval_number': [1],
            'application_recieved_date': ['Monday'],
            'completion_date': ['Tuesday'],
            'postal_code': ['ABCDEFG'],
            'vin': [123],
            'application_city_fuel': ['Zero Point One'],
            'incentive_type': ['A'],
            'incentive_cost': [0.50],
            'cheque_number': ['string'],
            'budget_code': ['string'],
            'scrap_date': ['string']
        }

        rename_columns = {
            'approval_number': 'Approval Num',
            'application_recieved_date': "App Recv'd Date",
            'completion_date': 'Completion Date',
            'postal_code': 'Postal Code',
            'vin': 'VIN',
            'application_city_fuel': 'App City Fuel',
            'incentive_type': 'Incentive Type',
            'incentive_cost': 'Incentive Cost',
            'cheque_number': 'Cheque #',
            'budget_code': 'Budget Code',
            'scrap_date': 'Scrap Date'
        }
            
        df = pd.DataFrame(data)
        df.rename(columns=rename_columns, inplace=True)
        excel_buffer = io.BytesIO()
        df.to_excel(excel_writer=excel_buffer, sheet_name='TOP OTHER TRANSACTIONS', index=False)
        excel_buffer.seek(0)

        response = import_from_xls(
            excel_file=excel_buffer,
            sheet_name='TOP OTHER TRANSACTIONS',
            model=ScrapIt,
            dataset_columns=ScrapItColumns,
            header_row=0,
            column_mapping_enum=ScrapItColumnMapping,
            field_types=self.field_types,
            replace_data=False,
            user='Tester',
            preparation_functions=[prepare_scrap_it]
        )

        self.assertFalse(response['success'])
        self.assertIn("Row 1: Incorrect type for 'vin'", response['errors'][0])
        self.assertIn("Row 1: Incorrect type for 'application_city_fuel'", response['errors'][1])

    def test_missing_columns(self):

        data = {
            'approval_number': [1],
            'application_recieved_date': ['Monday'],
            'completion_date': ['Tuesday'],
            'postal_code': ['ABCDEFG'],
            'incentive_type': ['A'],
            'incentive_cost': [0.50],
            'cheque_number': ['string'],
            'budget_code': ['string'],
            'scrap_date': ['string']
        }

        rename_columns = {
            'approval_number': 'Approval Num',
            'application_recieved_date': "App Recv'd Date",
            'completion_date': 'Completion Date',
            'postal_code': 'Postal Code',
            'incentive_type': 'Incentive Type',
            'incentive_cost': 'Incentive Cost',
            'cheque_number': 'Cheque #',
            'budget_code': 'Budget Code',
            'scrap_date': 'Scrap Date'
        }

        df = pd.DataFrame(data)
        df.rename(columns=rename_columns, inplace=True)
        excel_buffer = io.BytesIO()
        df.to_excel(excel_writer=excel_buffer, sheet_name='TOP OTHER TRANSACTIONS', index=False)
        excel_buffer.seek(0)

        response = import_from_xls(
            excel_file=excel_buffer,
            sheet_name='TOP OTHER TRANSACTIONS',
            model=ScrapIt,
            dataset_columns=ScrapItColumns,
            header_row=0,
            column_mapping_enum=ScrapItColumnMapping,
            field_types=self.field_types,
            replace_data=False,
            user='Tester',
            preparation_functions=[prepare_scrap_it]
        )

        self.assertFalse(response["success"])

        self.assertIn("Missing columns: VIN, App City Fuel", response["errors"][0])

    def test_missing_worksheet(self):

        data = {
            'approval_number': [1],
            'application_recieved_date': ['Monday'],
            'completion_date': ['Tuesday'],
            'postal_code': ['ABCDEFG'],
            'vin': ['string'],
            'application_city_fuel': [0.50],
            'incentive_type': ['A'],
            'incentive_cost': [0.50],
            'cheque_number': ['string'],
            'budget_code': ['string'],
            'scrap_date': ['string']
        }

        rename_columns = {
            'approval_number': 'Approval Num',
            'application_recieved_date': "App Recv'd Date",
            'completion_date': 'Completion Date',
            'postal_code': 'Postal Code',
            'vin': 'VIN',
            'application_city_fuel': 'App City Fuel',
            'incentive_type': 'Incentive Type',
            'incentive_cost': 'Incentive Cost',
            'cheque_number': 'Cheque #',
            'budget_code': 'Budget Code',
            'scrap_date': 'Scrap Date'
        }

        df = pd.DataFrame(data)
        df.rename(columns=rename_columns, inplace=True)
        excel_buffer = io.BytesIO()
        df.to_excel(excel_writer=excel_buffer, sheet_name='Wrong Sheet Name', index=False)
        excel_buffer.seek(0)

        response = import_from_xls(
            excel_file=excel_buffer,
            sheet_name='TOP OTHER TRANSACTIONS',
            model=ScrapIt,
            dataset_columns=ScrapItColumns,
            header_row=0,
            column_mapping_enum=ScrapItColumnMapping,
            field_types=self.field_types,
            replace_data=False,
            user='Tester',
            preparation_functions=[prepare_scrap_it]
        )

        self.assertFalse(response["success"])
        self.assertIn("Worksheet named 'TOP OTHER TRANSACTIONS' not found", response["errors"][0])

    #def test_user_missing_permission(self):
        #WIP