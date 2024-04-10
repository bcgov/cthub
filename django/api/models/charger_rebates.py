from auditable.models import Auditable
from django.db import models


class ChargerRebates(Auditable):

    organization = models.CharField(blank=True, null=True, max_length=250, unique=False)

    region = models.CharField(blank=True, null=True, max_length=200, unique=False)

    city = models.CharField(blank=True, null=True, max_length=200, unique=False)

    address = models.CharField(blank=True, null=True, max_length=200, unique=False)

    postal_code = models.CharField(blank=True, null=True, max_length=200, unique=False)

    number_of_fast_charging_stations = models.IntegerField(blank=True, null=True)

    in_service_date = models.CharField(
        blank=True, null=True, max_length=100, unique=False
    )

    expected_in_service_date = models.CharField(
        blank=True, null=True, max_length=200, unique=False
    )

    announced = models.CharField(blank=True, null=True, max_length=200, unique=False)

    rebate_paid = models.DecimalField(
        blank=True, null=True, max_digits=20, decimal_places=2
    )

    notes = models.CharField(blank=True, null=True, max_length=250, unique=False)

    class Meta:
        db_table = "charger_rebates"
