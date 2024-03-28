import urllib.request
import os
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from api.decorators.permission import check_upload_permission
from api.models.datasets import Datasets
from api.models.ldv_rebates import LdvRebates
from api.models.public_charging import PublicCharging
from api.models.charger_rebates import ChargerRebates
from api.models.speciality_use_vehicle_incentives import \
    SpecialityUseVehicleIncentives
from api.models.hydrogen_fueling import HydrogrenFueling
from api.models.scrap_it import ScrapIt
from api.models.arc_project_tracking import ARCProjectTracking
from api.models.data_fleets import DataFleets
from api.models.hydrogen_fleets import HydrogenFleets
from api.serializers.datasets import DatasetsSerializer
from api.services.minio import minio_get_object, minio_remove_object
from api.services.datasheet_template_generator import generate_template
from api.services.spreadsheet_uploader import import_from_xls
import api.constants as constants
from api.services.spreadsheet_uploader_prep import *

class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'put', 'get']

    @action(detail=False, methods=['get'])
    def datasets_list(self, request):
        
        incomplete_datasets = ['LDV Rebates', 'Specialty Use Vehicle Incentive Program', 'Public Charging -Remove Later', 'EV Charging Rebates', 'Hydrogen Fueling', 'Hydrogen Fleets', 'ARC Project Tracking', 'Data Fleets', 'Scrap It']

        datasets = Datasets.objects.all().exclude(name__in=incomplete_datasets)
        serializer = DatasetsSerializer(datasets, many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @method_decorator(check_upload_permission())
    def import_data(self, request):

        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        replace_data = request.data.get('replace', False)

        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)

            config = constants.DATASET_CONFIG.get(dataset_selected)
            if not config:
                return Response(f"Dataset '{dataset_selected}' is not supported.", status=status.HTTP_400_BAD_REQUEST)
            model = config['model']
            columns = config.get('columns')
            mapping = config.get('column_mapping')
            sheet_name = config.get('sheet_name', 'Sheet1')  # Default to 'Sheet1' if not specified
            preparation_functions = config.get('preparation_functions', [])
            validation_functions = config.get('validation_functions', [])
            header_row = config.get('header_row', 0)
               

            result = import_from_xls(
                excel_file=filename,
                sheet_name=sheet_name,
                model=model,
                header_row = header_row,
                preparation_functions=preparation_functions,
                validation_functions=validation_functions,
                dataset_columns=columns,
                column_mapping_enum=mapping,
                field_types=constants.FIELD_TYPES.get(dataset_selected),
                replace_data=replace_data,
                user = request.user
            )

            if not result['success']:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
        
        finally:      
            os.remove(filename)
            minio_remove_object(filename)
        
    
    @action(detail=False, methods=['get'])
    def download_dataset(self, request):
        dataset_name = request.GET.get('datasetSelected')
        if not dataset_name:
            return HttpResponse("Dataset name is required.", status=400)
        
        try:
            excel_file = generate_template(dataset_name)
            response = HttpResponse(
                excel_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{dataset_name}.xlsx"'
            return response
        except ValueError as e:
            return HttpResponse(str(e), status=400)