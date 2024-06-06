from django.db import models

from auditable.models import Auditable


class GoElectricRebates(Auditable):
    approvals = models.CharField(blank=False, null=False, max_length=20)
    date = models.DateField(max_length=20, null=False, blank=False)
    applicant_name = models.CharField(blank=False, null=False, max_length=250)
    max_incentive_amount_requested = models.IntegerField(
        null=True,
        blank=True,
    )
    category = models.CharField(blank=False, max_length=250, null=False)
    applicant_type = models.CharField(blank=True, max_length=50, null=True)
    incentive_paid = models.IntegerField(
        null=False,
        blank=False,
    )
    total_purchase_price = models.IntegerField(
        null=False,
        blank=False,
    )
    manufacturer = models.CharField(blank=False, max_length=250, null=False)
    model = models.CharField(blank=False, max_length=250, null=False)
    city = models.CharField(blank=False, max_length=250, null=False)
    postal_code = models.CharField(blank=True, max_length=250, null=True)
    phone = models.CharField(blank=False, max_length=20, null=False)
    email = models.CharField(blank=False, max_length=50, null=False)
    vin = models.CharField(blank=True, max_length=100, null=True)
    vehicle_class = models.CharField(blank=True, null=True, max_length=50)
    rebate_adjustment = models.CharField(blank=True, null=True, max_length=50)

    class Meta:
        db_table = "go_electric_rebates"
