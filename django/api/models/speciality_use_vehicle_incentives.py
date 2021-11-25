from django.db import models

from auditable.models import Auditable


class SpecialityUseVehicleIncentives(Auditable):
    approvals = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )
    date = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    applicant_name = models.CharField(
        blank=True,
        null=True,
        max_length=250
    )
    max_incentive_amount_requested = models.IntegerField(
        null=True,
        blank=True,
    )
    category = models.CharField(
        blank=True,
        max_length=250,
        null=True
    )
    applicant_type = models.CharField(
        blank=True,
        max_length=50,
        null=True
    )
    incentive_paid = models.IntegerField(
        null=True,
        blank=True,
    )
    total_purchase_price = models.IntegerField(
        null=True,
        blank=True,
    )
    manufacturer = models.CharField(
        blank=True,
        max_length=250,
        null=True
    )
    model = models.CharField(
        blank=True,
        max_length=250,
        null=True
    )

    class Meta:
        db_table = 'speciality_use_vehicle_incentives'
