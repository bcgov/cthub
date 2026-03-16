from django.db import models
from auditable.models import Auditable


class UploadedVinsFile(Auditable):
    filename = models.CharField(max_length=32, unique=True)

    # True when the upload is the ICBC dataset that requires full preprocessing
    # False for plain VIN lists (skip ICBC-specific parsing but still decode)
    icbc = models.BooleanField(default=True)

    chunksize = models.IntegerField(default=5000)

    start_index = models.IntegerField(default=0)

    chunks_per_iteration = models.IntegerField(default=100)

    processed = models.BooleanField(default=False)

    class Meta:
        db_table = "uploaded_vins_file"

    db_table_comment = "represents a file containing VINs, and parsing information"
