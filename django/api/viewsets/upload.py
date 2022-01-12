import urllib.request
import os

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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

class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'put', 'get']

    @action(detail=False, methods=['get'])
    def datasets_list(self, request):
        datasets = Datasets.objects.all()
        serializer = DatasetsSerializer(datasets, many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        replace_data = request.data.get('replace', False)
        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)
            if dataset_selected:
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
                    model.objects.all().delete()
                done = import_func(filename)
                if done:
                    os.remove(filename)
                    minio_remove_object(filename)

        except Exception as error:
            print('!!!!! error !!!!!!')
            print(error)
            return Response(status=400)

        return Response('success!', status=status.HTTP_201_CREATED)
