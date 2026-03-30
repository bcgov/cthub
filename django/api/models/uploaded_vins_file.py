from django.db import models
from django.contrib.postgres.fields import ArrayField
from auditable.models import Auditable


class UploadedVinsFile(Auditable):
    filename = models.CharField(max_length=32, unique=True)

    # True when the upload is the ICBC dataset that requires full preprocessing
    # False for plain VIN lists (skip ICBC-specific parsing but still decode)
    icbc = models.BooleanField(default=True)

    # null for non-icbc files;
    # for icbc files, this is the first snapshot date encountered;
    # need it for the "track removals" stage
    first_snapshot_date = models.DateField(null=True)

    # if the file is an icbc file and there exists a previous icbc file (say prev_file),
    # then this field tracks the byte offset of prev_file when the process is in the "tracking removed records" stage
    byte_offset = models.BigIntegerField(default=0)

    headers = ArrayField(models.TextField(), default=list)

    class FileStatus(models.TextChoices):
        # used by all files
        NEW = "NEW"
        SUCCESS = "SUCCESS"

        # used by non-icbc files
        PROCESSING = "PROCESSING"
        ERROR = "ERROR"

        # used by icbc files only
        ERROR_SAVING_DUPLICATES = "ERROR_SAVING_DUPLICATES"
        SUCCESS_SAVING_DUPLICATES = "SUCCESS_SAVING_DUPLICATES"
        TRACKING_CREATED_AND_MODIFIED_RECORDS = "TRACKING_CREATED_AND_MODIFIED_RECORDS"
        ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS = (
            "ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS"
        )
        SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS = (
            "SUCCESS_TRACKING_CREATED_AND_MODIFIED_RECORDS"
        )
        TRACKING_REMOVED_RECORDS = "TRACKING_REMOVED_RECORDS"
        ERROR_TRACKING_REMOVED_RECORDS = "ERROR_TRACKING_REMOVED_RECORDS"
        SUCCESS_TRACKING_REMOVED_RECORDS = "SUCCESS_TRACKING_REMOVED_RECORDS"
        ERROR_CLEARING_VIN_LOOKUP_TABLE = "ERROR_CLEARING_VIN_LOOKUP_TABLE"

    status = models.TextField(default=FileStatus.NEW, choices=FileStatus.choices)

    class Meta:
        db_table = "uploaded_vins_file"

    db_table_comment = "represents a file containing VINs, and parsing information"
