"""
Hydrogen Fueling
"""

from django.db import models

from api.models.mixins.effective_dates import EffectiveDates
from auditable.models import Auditable


class HydrogrenFueling(EffectiveDates, Auditable):

    class Meta:
        db_table = "hydrogen_fueling"

    station_number = models.IntegerField(null=True, blank=True)
    rfp_close_date = models.DateField(blank=True, null=True)
    station_name = models.CharField(blank=True, max_length=200, null=True)
    street_address = models.CharField(blank=True, max_length=200, null=True)
    city = models.CharField(blank=True, max_length=200, null=True, unique=False)
    postal_code = models.CharField(blank=True, max_length=50, null=True, unique=False)
    proponent = models.CharField(blank=True, max_length=100, null=True)
    location_partner = models.CharField(max_length=100, null=True, blank=True)
    capital_funding_awarded = models.DecimalField(
        null=True, blank=True, max_digits=20, decimal_places=2
    )
    om_funding_potential = models.DecimalField(
        null=True, blank=True, max_digits=20, decimal_places=2
    )
    daily_capacity = models.IntegerField(null=True, blank=True)
    bar_700 = models.BooleanField(default=False)
    bar_350 = models.BooleanField(default=False)
    status = models.CharField(blank=True, max_length=200, null=True, unique=False)
    number_of_fueling_positions = models.IntegerField(null=True, blank=True)
    operational_date = models.DateField(blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    total_capital_cost = models.DecimalField(max_digits=20, decimal_places=2)
