from auditable.models import Auditable
from django.db import models


class HydrogenFleets(Auditable):
    application_number = models.IntegerField(blank=True, null=True)

    fleet_number = models.IntegerField(blank=True, null=True)

    application_date = models.CharField(
        blank=True, null=True, max_length=100, unique=False
    )

    organization_name = models.CharField(
        blank=True, null=True, max_length=250, unique=False
    )

    fleet_name = models.CharField(blank=True, null=True, max_length=250, unique=False)

    street_address = models.CharField(
        blank=True, null=True, max_length=250, unique=False
    )

    city = models.CharField(blank=True, null=True, max_length=100, unique=False)

    postal_code = models.CharField(blank=True, null=True, max_length=10, unique=False)

    vin = models.CharField(blank=True, null=True, max_length=20, unique=False)

    make = models.CharField(blank=True, null=True, max_length=100, unique=False)

    model = models.CharField(blank=True, null=True, max_length=100, unique=False)

    year = models.CharField(blank=True, null=True, max_length=100, unique=False)

    purchase_date = models.CharField(
        blank=True, null=True, max_length=100, unique=False
    )

    dealer_name = models.CharField(blank=True, null=True, max_length=250, unique=False)

    rebate_amount = models.CharField(
        blank=True, null=True, max_length=250, unique=False
    )

    class Meta:
        db_table = "hydrogen_fleets"
