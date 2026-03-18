from django.db import models
from auditable.models import Auditable
from django.utils.translation import gettext_lazy as _


class UploadedVinRecord(Auditable):
    vin = models.TextField(unique=True)

    vpic_decode_successful = models.BooleanField(default=False)

    vpic_number_of_decode_attempts = models.IntegerField(default=0)

    vinpower_decode_successful = models.BooleanField(default=False)

    vinpower_number_of_decode_attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "uploaded_vin_record"

    db_table_comment = "represents an uploaded VIN, and associated information"
