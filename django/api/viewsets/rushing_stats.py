"""
Viewset for Rushing stats
"""
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from api.filters.rushing_stats import RushingStatsFilter
from api.models.rushing_stats import RushingStats
from api.serializers.rushing_stats import RushingStatsSerializer


class RushingStatsViewset(GenericViewSet, ListModelMixin):
    """
    This will build the list view and tie it with the serializer and
    permissions
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get']
    filterset_class = RushingStatsFilter
    ordering_fields = '__all_related__'
    ordering = ('player__last_name', 'player__first_name',)

    serializer_classes = {
        'default': RushingStatsSerializer
    }

    def get_queryset(self):
        queryset = RushingStats.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')
