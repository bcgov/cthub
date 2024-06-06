"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework.serializers import ModelSerializer

from api.models.icbc_registration_data import IcbcRegistrationData
from api.serializers.icbc_vehicle import IcbcVehicleSerializer


class IcbcRegistrationDataSerializer(ModelSerializer):
    """
    Default Serializer for ICBC Vehicle
    """

    icbc_vehicle = IcbcVehicleSerializer()

    class Meta:
        model = IcbcRegistrationData
        fields = "__all__"
