import urllib.request
import os
from django.db.models import query
from api.services.ldv_rebates import import_from_xls
from api.services.minio import minio_get_object, minio_remove_object
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from api.models.datasets import Datasets
from api.serializers.datasets import DatasetsSerializer
from api.models.ldv_rebates import LdvRebates

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
        user = request.user
        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        replace_data = request.data.get('replaceData', False)

        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)
            if dataset_selected:
                if dataset_selected == 'LDV Rebates':
                    if replace_data:
                        LdvRebates.objects.all().delete()
                    done = import_from_xls(filename)
                    if done:
                        os.remove(filename)
                        minio_remove_object(filename)

        except Exception as error:
            print('!!!!! error !!!!!!')
            print(error)
            return Response(status=400)

        return Response('success!', status=status.HTTP_201_CREATED)
