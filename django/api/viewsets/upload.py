import urllib.request
import os
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from api.decorators.whitelisted_users import check_whitelist
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
from api.services.arc_project_tracking import import_from_xls as \
    import_arc_project_tracking
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

class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'put', 'get']

    @action(detail=False, methods=['get'])
    def datasets_list(self, request):
        datasets = Datasets.objects.all()
        serializer = DatasetsSerializer(datasets, many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @method_decorator(check_whitelist())
    def import_data(self, request):
        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        replace_data = request.data.get('replace', False)
        error = ''
        done = ''
        records_inserted = 0
        starting_count = 0
        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)
            if dataset_selected:
                model = ''
                done = ''
                import_func = ''
                if dataset_selected == 'EV Charging Rebates':
                    import_func = import_charger_rebates
                    model = ChargerRebates
                if dataset_selected == 'LDV Rebates':
                    import_func = import_ldv
                    model = LdvRebates
                if dataset_selected == 'Hydrogen Fueling':
                    import_func = import_hydrogen_fueling
                    model = HydrogrenFueling
                if dataset_selected == \
                        'Specialty Use Vehicle Incentive Program':
                    import_func = import_suvi
                    model = SpecialityUseVehicleIncentives
                if dataset_selected == 'Public Charging':
                    import_func = import_public_charging
                    model = PublicCharging
                if dataset_selected == 'Scrap It':
                    import_func = import_scrap_it
                    model = ScrapIt
                if dataset_selected == 'ARC Project Tracking':
                    import_func = import_arc_project_tracking
                    model = ARCProjectTracking
                if dataset_selected == 'Data Fleets':
                    import_func = import_data_fleets
                    model = DataFleets
                if dataset_selected == 'Hydrogen Fleets':
                    import_func = import_hydrogen_fleets
                    model = HydrogenFleets
                if replace_data:
                    starting_count = 0
                    model.objects.all().delete()
                else:
                    starting_count = model.objects.all().count()
                done = import_func(filename)
                if done:
                    os.remove(filename)
                    minio_remove_object(filename)
        except Exception as error:
            done = (error, 'file')
        final_count = model.objects.all().count()
        records_inserted = final_count - starting_count
        records_inserted_msg = "{} records inserted. This table currently contains {} records.".format(records_inserted, final_count)
        if done != True:
            try:
                error_location = done[1]
                error = done[0]
                error_row = 0
                error_msg = "There was an error. Please check your file and ensure you have the correctly named worksheets, column names, and data types in cells and reupload. Error: {}".format(error)
                if len(done) > 2:
                    error_row = done[2]
                error_type = type(error).__name__
                field_names = [f.name for f in model._meta.fields]   
                if error_location == 'data':
                    if error_type in (type(LookupError), type(KeyError), 'KeyError') :
                        error_msg = "Please make sure you've uploaded a file with the correct data including the correctly named columns. There was an error finding: {}. This dataset requires the following columns: {}".format(error, field_names)
                    elif error_type == 'ValueError' or type(ValueError):
                        ## note for next batch of scripts, possibly add str(type(ValueError)) 
                        ## to this but check for impacts to other exceptions
                        error_msg = "{} on row {}. Please make sure you've uploaded a file with the correct data.".format(error, error_row)
                    elif isinstance(error, ValidationError):
                        error_msg ="Issue with cell value on row {}. {}".format(error_row, str(error)[2:-2])
                elif error_location == 'file':
                    error_msg = "{}. Please make sure you've uploaded a file with the correct data including the correctly named worksheets.".format(error)
                if error_msg[-1] != '.':
                    error_msg+='.'
                error_msg += records_inserted_msg
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(error)
                return Response('There was an issue!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(records_inserted_msg, status=status.HTTP_201_CREATED)
        
    
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