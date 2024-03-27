from auditable.models import Auditable
from django.db import models


class ScrapIt(Auditable):

    approval_number = models.IntegerField(
        blank=True,
        null=True
    )

    application_received_date = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    completion_date = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    postal_code = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    vin = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    application_city_fuel = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        unique=False
    )

    incentive_type = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    incentive_cost = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        unique=False
    )

    cheque_number = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    budget_code = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    scrap_date = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    class Meta:
        db_table = "scrap_it"