"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework.serializers import ModelSerializer

from api.models.rushing_stats import RushingStats
from api.serializers.player import PlayerSerializer


class RushingStatsSerializer(ModelSerializer):
    """
    Default Serializer for Rushing Stats
    """
    player = PlayerSerializer()

    class Meta:
        model = RushingStats
        fields = '__all__'
