from django.db import models
from auditable.models import Auditable
from django.utils.translation import gettext_lazy as _


class UploadedVinRecord(Auditable):
    vin = models.CharField(max_length=17, unique=True)

    class Change(models.TextChoices):
        CREATED = ("created", _("Created"))
        MODIFIED = ("modified", _("Modified"))
        REMOVED = ("removed", _("Removed"))

    change = models.CharField(
        max_length=64,
        default=Change.CREATED,
        choices=Change.choices,
    )

    data = models.JSONField()

    vpic_current_decode_successful = models.BooleanField(default=False)

    vpic_number_of_current_decode_attempts = models.IntegerField(default=0)

    vinpower_current_decode_successful = models.BooleanField(default=False)

    vinpower_number_of_current_decode_attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "uploaded_vin_record"

    db_table_comment = "represents an uploaded VIN, and associated information"
