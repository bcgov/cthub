from django.db import models
from auditable.models import Auditable


class DecodedVinRecord(Auditable):
    vin = models.CharField(max_length=17, unique=True)

    data = models.JSONField()

    class Meta:
        abstract = True


class VpicDecodedVinRecord(DecodedVinRecord):
    class Meta:
        db_table = "vpic_decoded_vin_record"


class VinpowerDecodedVinRecord(DecodedVinRecord):
    class Meta:
        db_table = "vinpower_decoded_vin_record"
