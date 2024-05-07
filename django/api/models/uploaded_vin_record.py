from django.db import models
from auditable.models import Auditable


class UploadedVinRecord(Auditable):
    vin = models.CharField(max_length=17)

    postal_code = models.CharField(max_length=7, null=True, blank=True)

    data = models.JSONField()

    vpic_current_decode_successful = models.BooleanField(default=False)

    vpic_number_of_current_decode_attempts = models.IntegerField(default=0)

    vinpower_current_decode_successful = models.BooleanField(default=False)

    vinpower_number_of_current_decode_attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "uploaded_vin_record"
        constraints = [
            models.UniqueConstraint(
                fields=["vin", "postal_code"], name="unique_vin_postal_code"
            )
        ]
