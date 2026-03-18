from django.db import models
from auditable.models import Auditable
from django.utils.translation import gettext_lazy as _


class UploadedVinsFile(Auditable):
    filename = models.CharField(max_length=32, unique=True)

    # True when the upload is the ICBC dataset that requires full preprocessing
    # False for plain VIN lists (skip ICBC-specific parsing but still decode)
    icbc = models.BooleanField(default=True)

    chunksize = models.IntegerField(default=5000)

    start_index = models.IntegerField(default=0)

    chunks_per_iteration = models.IntegerField(default=100)

    class FileStatus(models.TextChoices):
        ERROR = ("error", _("Error"))
        PROCESSING = ("processing", _("Processing"))
        SUCCESS = ("success", _("Success"))

    status = models.TextField(default=FileStatus.PROCESSING, choices=FileStatus.choices)

    class Meta:
        db_table = "uploaded_vins_file"

    db_table_comment = "represents a file containing VINs, and parsing information"
