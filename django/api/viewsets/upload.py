import urllib.request
import os
from api.services.ldv_rebates import import_from_xls
from api.services.minio import minio_get_object, minio_remove_object
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet


class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'put']
 
    @action(detail=False, methods=['post'])
    def import_data(self, request):
        user = request.user
        filename = request.data.get('filename')
        dataset_selected = request.data.get('datasetSelected')
        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)
            if dataset_selected:
                if dataset_selected == 'LDV rebates':
                    done = import_from_xls(filename)
                if done:
                    os.remove(filename)
                    minio_remove_object(filename)

        except Exception as error:
            print('!!!!! error !!!!!!')
            print(error)
            return Response(status=400)

        return Response('success!', status=status.HTTP_201_CREATED)
