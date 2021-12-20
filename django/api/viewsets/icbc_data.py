"""
Viewset for ICBC Data
"""
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from api.filters.icbc_data import IcbcDataFilter
from api.models.icbc_registration_data import IcbcRegistrationData
from api.serializers.icbc_registration_data import \
    IcbcRegistrationDataSerializer


class IcbcViewset(GenericViewSet, ListModelMixin):
    """
    This will build the list view and tie it with the serializer and
    permissions
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get']
    filterset_class = IcbcDataFilter
    ordering_fields = '__all_related__'
    ordering = ('icbc_vehicle__make',)

    serializer_classes = {
        'default': IcbcRegistrationDataSerializer
    }

    def get_queryset(self):
        queryset = IcbcRegistrationData.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')
