from auditable.models import Auditable
from django.db import models


class LdvRebates(Auditable):
    submission_id = models.IntegerField(unique=False)
    casl_consent = models.BooleanField(default=False)
    date_approved = models.CharField(
        blank=True, null=True, max_length=100, unique=False
    )
    submission_date = models.CharField(
        blank=True, null=True, max_length=100, unique=False
    )
    company_name = models.CharField(blank=True, max_length=200, null=True, unique=False)
    company_city = models.CharField(blank=True, max_length=200, null=True, unique=False)
    applicant_name = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    applicant_address_1 = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    applicant_address_2 = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    applicant_city = models.CharField(
        blank=True, max_length=100, null=True, unique=False
    )
    applicant_postal_code = models.CharField(
        blank=True, max_length=50, null=True, unique=False
    )

    applicant_phone = models.CharField(
        blank=True, max_length=25, null=True, unique=False
    )
    applicant_email = models.CharField(
        blank=True, max_length=200, null=True, unique=False
    )
    applicant_use = models.CharField(blank=True, max_length=50, null=True, unique=False)
    applicant_type = models.CharField(
        blank=True, max_length=100, null=True, unique=False
    )
    business_name = models.CharField(
        blank=True, max_length=100, null=True, unique=False
    )
    business_number = models.CharField(
        blank=True, max_length=50, null=True, unique=False
    )
    drivers_license = models.CharField(
        blank=True, max_length=50, null=True, unique=False
    )
    province = models.CharField(
        blank=True,
        max_length=50,
        null=True,
        unique=False,
    )
    msrp = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    other_incentives = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    document_type = models.CharField(blank=True, max_length=50, null=True, unique=False)
    vehicle = models.CharField(blank=True, max_length=200, null=True, unique=False)
    incentive_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    vin = models.CharField(blank=True, max_length=255, null=True, unique=False)
    delivered = models.BooleanField(default=False)
    consent_to_contact = models.BooleanField(default=False)

    class Meta:
        db_table = "ldv_rebates"
