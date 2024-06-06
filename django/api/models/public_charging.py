"""
Public Charging Model
"""

from django.db import models

from api.models.mixins.effective_dates import EffectiveDates
from auditable.models import Auditable


class PublicCharging(EffectiveDates, Auditable):

    class Meta:
        db_table = "public_charging"

    applicant_name = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    city = models.CharField(blank=True, max_length=200, null=True, unique=False)
    postal_code = models.CharField(blank=True, max_length=50, null=True, unique=False)
    address = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    charging_station_info = models.CharField(
        blank=True,
        max_length=500,
        null=True,
    )
    between_25kw_and_50kw = models.IntegerField(null=True, blank=True)
    between_50kw_and_100kw = models.IntegerField(null=True, blank=True)
    over_100kw = models.IntegerField(null=True, blank=True)
    level_2_units = models.IntegerField(null=True, blank=True)
    level_2_ports = models.IntegerField(null=True, blank=True)
    estimated_budget = models.DecimalField(max_digits=20, decimal_places=2)
    adjusted_rebate = models.DecimalField(max_digits=20, decimal_places=2)
    rebate_percent_maximum = models.DecimalField(max_digits=3, decimal_places=2)
    pilot_project = models.BooleanField()
    region = models.CharField(blank=True, max_length=200, null=True, unique=False)
    organization_type = models.CharField(
        blank=True, max_length=100, null=True, unique=False
    )
    project_status = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    review_number = models.IntegerField(null=True, blank=True)
    rebate_paid = models.DecimalField(max_digits=20, decimal_places=2)
