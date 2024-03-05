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
from api.services.ldv_rebates import import_from_xls as import_ldv
from api.services.hydrogen_fueling import import_from_xls as \
    import_hydrogen_fueling
from api.services.charger_rebates import import_from_xls as \
    import_charger_rebates
from api.services.scrap_it import import_from_xls as \
    import_scrap_it
from api.services.data_fleets import import_from_xls as \
    import_data_fleets
from api.services.hydrogen_fleets import import_from_xls as \
    import_hydrogen_fleets
from api.services.minio import minio_get_object, minio_remove_object
from api.services.public_charging import import_from_xls as \
    import_public_charging
from api.services.speciality_use_vehicle_incentives import \
    import_from_xls as import_suvi
from api.services.datasheet_template_generator import generate_template
from api.services.spreadsheet_uploader import import_from_xls
from api.constants import *
from api.services.spreadsheet_uploader_prep import prepare_arc_project_tracking

class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'put', 'get']

    @action(detail=False, methods=['get'])
    def datasets_list(self, request):
        datasets = Datasets.objects.all()
        serializer = DatasetsSerializer(datasets, many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @method_decorator(check_upload_permission())
    def import_data(self, request):

        DATASET_CONFIG = {
        'ARC Project Tracking': {
            'model': ARCProjectTracking,
            'columns': ARCProjectTrackingColumns,
            'column_mapping': ArcProjectTrackingColumnMapping,
            'sheet_name': 'Project_Tracking',
            'preparation_functions': [prepare_arc_project_tracking]
        }
    }

        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        replace_data = request.data.get('replace', False)

        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)

            config = DATASET_CONFIG.get(dataset_selected)
            if not config:
                return Response(f"Dataset '{dataset_selected}' is not supported.", status=status.HTTP_400_BAD_REQUEST)
            model = config['model']
            columns = config.get('columns')
            mapping = config.get('column_mapping')
            sheet_name = config.get('sheet_name', 'Sheet1')  # Default to 'Sheet1' if not specified
            preparation_functions = config.get('preparation_functions', [])
            validation_functions = config.get('validation_functions', [])

            if replace_data:
                model.objects.all().delete()

            result = import_from_xls(
                excel_file=filename,
                dataset_name=dataset_selected,
                sheet_name=sheet_name,
                model=model,
                preparation_functions=preparation_functions,
                validation_functions=validation_functions,
                dataset_columns=columns,
                column_mapping_enum=mapping,
                field_types=FIELD_TYPES
            )

            if not result['success']:
                return Response(result['errors'], status=status.HTTP_400_BAD_REQUEST)
            return Response(result['message'], status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"An exception occurred: {str(e)}")
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