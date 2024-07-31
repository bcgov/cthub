from django.db import models

from tfrs.models.DocumentCategory import DocumentCategory
from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.EffectiveDates import EffectiveDates


class DocumentType(Auditable, EffectiveDates):
    the_type = models.CharField(max_length=100, blank=True, null=True, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    category = models.ForeignKey(
        DocumentCategory,
        blank=False,
        null=False,
        unique=False,
        related_name="types",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = "document_type"
