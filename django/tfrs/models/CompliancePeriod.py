from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DisplayOrder import DisplayOrder
from tfrs.models.mixins.EffectiveDates import EffectiveDates


class CompliancePeriod(Auditable, DisplayOrder, EffectiveDates):
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "compliance_period"
