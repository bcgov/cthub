
from rest_framework.serializers import ModelSerializer

from api.models.datasets import Datasets


class DatasetsSerializer(ModelSerializer):

    class Meta:
        model = Datasets
        fields = ('name', 'id')
