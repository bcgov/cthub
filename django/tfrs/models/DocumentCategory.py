from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DisplayOrder import DisplayOrder


class DocumentCategory(Auditable, DisplayOrder):
    name = models.CharField(max_length=120, blank=True, null=True, unique=True)

    class Meta:
        db_table = "document_category"
