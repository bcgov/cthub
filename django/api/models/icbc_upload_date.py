from django.db import models
from auditable.models import Auditable


class IcbcUploadDate(Auditable):
    upload_date = models.DateField(
        blank=False,
        null=False,
        auto_now=False
    )

    class Meta:
        db_table = 'icbc_upload_date'
