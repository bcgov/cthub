import uuid

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.decorators import method_decorator
from api.decorators.permission import check_upload_permission
from api.services.minio import minio_put_object


class MinioViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ["get"]

    @action(detail=False, methods=["get"])
    @method_decorator(check_upload_permission())
    def put(self, request):
        object_name = uuid.uuid4().hex
        url = minio_put_object(object_name)

        return Response({"url": url, "minio_object_name": object_name})
