from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DisplayOrder import DisplayOrder
from tfrs.models.mixins.EffectiveDates import EffectiveDates


class CreditTradeType(Auditable, DisplayOrder, EffectiveDates):
    the_type = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
    )
    is_gov_only_type = models.BooleanField()

    class Meta:
        db_table = "credit_trade_type"
