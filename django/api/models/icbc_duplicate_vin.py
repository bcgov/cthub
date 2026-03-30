from django.db import models


class IcbcDuplicateVin(models.Model):
    vin = models.TextField(unique=True)

    class Meta:
        db_table = "icbc_duplicate_vin"
