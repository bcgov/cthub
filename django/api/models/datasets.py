from django.db import models
from auditable.models import Auditable


class Datasets(Auditable):
    name = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=50,
    )

    class Meta:
        db_table = "datasets"
