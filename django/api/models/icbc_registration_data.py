from auditable.models import Auditable
from django.db import models


class IcbcRegistrationData(Auditable):
    icbc_vehicle = models.ForeignKey(
        'IcbcVehicle',
        related_name=None,
        on_delete=models.CASCADE
    )

    vin = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=20,
        db_index=True
    )

    icbc_upload_date = models.ForeignKey(
        'IcbcUploadDate',
        related_name=None,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "icbc_registration_data"
