from django.db import models
from auditable.models import Auditable


class UploadedVinsFile(Auditable):
    filename = models.CharField(max_length=32, unique=True)

    chunk_size = models.IntegerField(default=25000)

    chunks_per_run = models.IntegerField(default=4)

    start_index = models.IntegerField(default=0)

    processed = models.BooleanField(default=False)

    class Meta:
        db_table = "uploaded_vins_file"

