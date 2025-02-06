from auditable.models import Auditable
from django.db import models


class ARCProjectTracking(Auditable):

    reference_number = models.CharField(
        blank=False, null=False, max_length=50, unique=False
    )

    proponent = models.CharField(blank=False, null=False, max_length=500, unique=False)

    status = models.CharField(blank=False, null=False, max_length=250, unique=False)

    funding_call = models.CharField(blank=False, null=False, max_length=50, unique=False)

    project_title = models.CharField(
        blank=False, null=False, max_length=500, unique=False
    )

    vehicle_category = models.CharField(
        blank=False, null=False, max_length=250
    )

    zev_sub_sector = models.CharField(
        blank=True, null=True, max_length=250, unique=False
    )

    fuel_type = models.CharField(blank=True, null=True, max_length=250, unique=False)

    retrofit = models.CharField(blank=True, null=True, max_length=250)

    primary_location = models.CharField(
        blank=False, null=False, max_length=250, unique=False
    )

    economic_region = models.CharField(
        blank=False, null=False, max_length=250
    )

    jobs = models.IntegerField(blank=True, null=True)

    funds_commited = models.IntegerField(blank=False, null=False)

    funds_disbursed = models.IntegerField(blank=True, null=True)
    
    remaining_disbursed = models.IntegerField(blank=True, null=True)

    total_project_value = models.IntegerField(blank=True, null=True)

    start_date = models.DateField(blank=True, null=True, unique=False)

    completion_date = models.DateField(
        blank=True, null=True, unique=False
    )

    complete_or_termination_date = models.DateField(
        blank=True, null=True, unique=False
    )

    publicly_announced = models.CharField(blank=True, null=True, max_length=250)

    notes = models.CharField(blank=True, null=True, max_length=250)

    class Meta:
        db_table = "arc_project_tracking"
