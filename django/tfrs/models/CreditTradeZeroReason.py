from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DisplayOrder import DisplayOrder
from tfrs.models.mixins.EffectiveDates import EffectiveDates


class CreditTradeZeroReason(Auditable, DisplayOrder, EffectiveDates):
    reason = models.CharField(max_length=25)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'credit_trade_zero_reason'
