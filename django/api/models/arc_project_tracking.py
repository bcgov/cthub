from auditable.models import Auditable
from django.db import models


class ARCProjectTracking(Auditable):

    funding_call = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        unique=False
    )

    proponent = models.CharField(
        blank=True,
        null=False,
        max_length=500,
        unique=False
    )

    reference_number = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        unique=False
    )

    project_title = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        unique=False
    )

    primary_location = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    status = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    arc_funding = models.IntegerField(
        blank=True,
        null=True
    )

    funds_issued = models.IntegerField(
        blank=True,
        null=True
    )

    start_date = models.CharField(
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

    total_project_value = models.IntegerField(
        blank=True,
        null=True
    )

    zev_sub_sector = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    on_road_off_road = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    fuel_type = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )

    publicly_announced = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "arc_project_tracking"