"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework.serializers import ModelSerializer, SlugRelatedField

from api.models.icbc_vehicle import IcbcVehicle


class IcbcVehicleSerializer(ModelSerializer):
    """
    Default Serializer for ICBC Vehicle
    """

    model_year = SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = IcbcVehicle
        fields = "__all__"
