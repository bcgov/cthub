from django.db import models


class IcbcVinLookup(models.Model):
    vin = models.TextField(unique=True)

    class Meta:
        db_table = "icbc_vin_lookup"
