from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DisplayOrder import DisplayOrder
from tfrs.models.mixins.EffectiveDates import EffectiveDates


class CreditTradeStatus(Auditable, DisplayOrder, EffectiveDates):
    status = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True
    )
    description = models.CharField(
        max_length=4000,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'credit_trade_status'
