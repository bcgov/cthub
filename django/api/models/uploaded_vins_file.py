from django.db import models
from django.contrib.postgres.fields import ArrayField
from auditable.models import Auditable


class UploadedVinsFile(Auditable):
    filename = models.CharField(max_length=32, unique=True)

    # True when the upload is the ICBC dataset that requires full preprocessing
    # False for plain VIN lists (skip ICBC-specific parsing but still decode)
    icbc = models.BooleanField(default=True)

    headers = ArrayField(models.TextField())

    headers_byte_length = models.IntegerField()

    # where to begin reading the file
    byte_offset = models.BigIntegerField(default=0)

    # null for non-icbc files;
    # for icbc files, this is the first snapshot date encountered;
    # need it for the "track removals" stage
    first_snapshot_date = models.DateField(null=True)

    # null for non-icbc files;
    # for icbc files, this is used to track where we are in the "track removals" stage
    last_encountered_vin = models.TextField(null=True)

    class FileStatus(models.TextChoices):
        # used by all files
        NEW = "NEW"
        SUCCESS = "SUCCESS"

        # used by non-icbc files
        PROCESSING = "PROCESSING"
        ERROR = "ERROR"

        # used by icbc files only
        SUCCESS_SAVING_FIRST_SNAPSHOT_DATE = "SUCCESS_SAVING_FIRST_SNAPSHOT_DATE"
        ERROR_SAVING_FIRST_SNAPSHOT_DATE = "ERROR_SAVING_FIRST_SNAPSHOT_DATE"

        SAVING_DUPLICATES_AND_LOOKUPS = "SAVING_DUPLICATES_AND_LOOKUPS"
        SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS = "SUCCESS_SAVING_DUPLICATES_AND_LOOKUPS"
        ERROR_SAVING_DUPLICATES_AND_LOOKUPS = "ERROR_SAVING_DUPLICATES_AND_LOOKUPS"

        TRACKING_REMOVED_RECORDS = "TRACKING_REMOVED_RECORDS"
        SUCCESS_TRACKING_REMOVED_RECORDS = "SUCCESS_TRACKING_REMOVED_RECORDS"
        ERROR_TRACKING_REMOVED_RECORDS = "ERROR_TRACKING_REMOVED_RECORDS"

        TRACKING_CREATED_AND_MODIFIED_RECORDS = "TRACKING_CREATED_AND_MODIFIED_RECORDS"
        ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS = (
            "ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS"
        )

    status = models.TextField(default=FileStatus.NEW, choices=FileStatus.choices)

    class Meta:
        db_table = "uploaded_vins_file"

    db_table_comment = "represents a file containing VINs, and parsing information"
