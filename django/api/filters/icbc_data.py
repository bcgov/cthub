"""
Filter instructions for the model: RushingStats.
By default, all columns can be filtered by passing a GET parameter to the
URL with the respective column name.
e.g. /api/rushing-stats?att_per_game=1
     /api/rushing-stats?player__first_name=Joe
Further reading:
https://django-filter.readthedocs.io/en/master/ref/filters.html
"""
from django.db.models import Q
from django_filters import FilterSet, CharFilter

from api.models.icbc_registration_data import IcbcRegistrationData


class IcbcDataFilter(FilterSet):
    icbc_vehicle__make = CharFilter(lookup_expr='icontains')
    icbc_vehicle__model_name = CharFilter(lookup_expr='icontains')
    icbc_vehicle__model_year__name = CharFilter(lookup_expr='icontains')
    vin = CharFilter(lookup_expr='icontains')

    class Meta:
        model = IcbcRegistrationData
        fields = [
            'vin',
        ]
