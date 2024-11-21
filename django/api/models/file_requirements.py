from django.db import models
from auditable.models import Auditable
from api.models.datasets import Datasets


class FileRequirements(Auditable):
    dataset = models.OneToOneField(
        Datasets,
        related_name="file_requirements",
        on_delete=models.CASCADE,
    )

    sheet = models.TextField(blank=True, null=True)

    columns = models.TextField(blank=True, null=True)

    formats = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "file_requirements"
