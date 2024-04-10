from django.db import models

from auditable.models import Auditable


class VINDecodedInformation(Auditable):
    vin = models.CharField(blank=False, null=False, max_length=20)
    manufacturer = models.CharField(max_length=500, null=True, blank=True)
    make = models.CharField(blank=True, null=True, max_length=250)
    model = models.CharField(blank=True, max_length=250, null=True)
    model_year = models.IntegerField(
        null=True,
        blank=True,
    )
    fuel_type_primary = models.CharField(blank=True, max_length=250, null=True)

    class Meta:
        db_table = "vin_decoded_information"
