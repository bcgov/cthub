from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status


class HealthCheckViewset(GenericViewSet):
    authentication_classes = []
    permission_classes=[]

    def list(self, request):
        return Response(status=status.HTTP_200_OK)