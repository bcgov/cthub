from django.db import models

from tfrs.models.CompliancePeriod import CompliancePeriod
from tfrs.models.DocumentStatus import DocumentStatus
from tfrs.models.DocumentType import DocumentType


class DocumentData(models.Model):
    """Common fields for Document and DocumentHistory"""

    title = models.CharField(
        max_length=120,
        blank=False
    )

    status = models.ForeignKey(
        DocumentStatus,
        on_delete=models.PROTECT,
        null=False
    )

    type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        null=False
    )

    compliance_period = models.ForeignKey(
        CompliancePeriod,
        on_delete=models.PROTECT,
        null=False
    )

    milestone = models.CharField(
        blank=True, max_length=1000, null=True
    )

    class Meta:
        abstract = True
