from auditable.models import Auditable
from django.db import models

class LdvData(Auditable):

    applicant_type = models.CharField(
        max_length=100, unique=False, blank=False, null=False
    )

    application_id = models.CharField(
        max_length=100, unique=True, blank=False, null=False
    )

    dealership_name = models.CharField(
        max_length=100, unique=False, blank=False, null=False
    )

    date_submitted = models.DateField(
        blank=False, null=False
    )

    payment_dt = models.DateField(
        blank=False, null=False
    )

    bc_drivers_license_no = models.CharField(
        max_length=100, blank=False, null=False
    )

    bc_inc_no = models.CharField(
        max_length=100, blank=False, null=False
    )

    eligible_rebate_amt = models.IntegerField(
        blank=False, null=False
    )

    sale_type = models.CharField(
        max_length=100, unique=False, blank=True, null=True
    )

    vin = models.CharField(
        max_length=17, blank=False, null=False
    )

    year = models.IntegerField(
        unique=False, blank=False, null=False
    )

    manufacturer = models.CharField(
        max_length=100, unique=False, blank=False, null=False
    )

    model = models.CharField(
        max_length=100, unique=False, blank=True, null=True
    )

    trim = models.CharField(
        max_length=100, unique=False, blank=True, null=True
    )

    vehicle_type = models.CharField(
        max_length=50, unique=False, blank=True, null=True
    )

    vehicle_class = models.CharField(
        max_length=50, unique=False, blank=True, null=True
    )

    msrp = models.IntegerField(
        unique=False, blank=True, null=True
    )

    electric_range = models.IntegerField(
        unique=False, blank=True, null=True
    )

    vin_token = models.CharField(
        max_length=9, unique=False, blank=True, null=True
    )

    city = models.CharField(
        max_length=100, unique=False, blank=True, null=True
    )

    postal_code = models.CharField(
        max_length=10, unique=False, blank=True, null=True
    )

    business_corp_name = models.CharField(
        max_length=200, unique=False, blank=True, null=True
    )

    car_share_name = models.CharField(
        max_length=200, unique=False, blank=True, null=True
    )

    non_profit_name = models.CharField(
        max_length=200, unique=False, blank=True, null=True
    )

    municipality_name = models.CharField(
        max_length=200, unique=False, blank=True, null=True
    )

    date_of_delivery = models.DateField(
        blank=True, null=True
    )

    lease_term = models.CharField(
        max_length=50, unique=False, blank=True, null=True
    )

    class Meta:
        db_table = "ldv_data"
