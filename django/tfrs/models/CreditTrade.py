from decimal import Decimal
from django.db import models
from django.db.models import ManyToManyField

from tfrs.models.mixins.Auditable import Auditable

from .CompliancePeriod import CompliancePeriod
from .CreditTradeStatus import CreditTradeStatus
from .CreditTradeType import CreditTradeType
from .CreditTradeZeroReason import CreditTradeZeroReason
from .Organization import Organization


class CreditTrade(Auditable):
    status = models.ForeignKey(
        CreditTradeStatus,
        related_name='credit_trades',
        on_delete=models.PROTECT
    )
    initiator = models.ForeignKey(
        Organization,
        related_name='initiator_credit_trades',
        blank=True, null=True,
        on_delete=models.PROTECT
    )
    respondent = models.ForeignKey(
        Organization,
        related_name='respondent_credit_trades',
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        CreditTradeType,
        related_name='credit_trades',
        on_delete=models.PROTECT
    )
    number_of_credits = models.IntegerField()
    fair_market_value_per_credit = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    zero_reason = models.ForeignKey(
        CreditTradeZeroReason,
        related_name='credit_trades',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    trade_effective_date = models.DateField(
        blank=True,
        null=True,
    )
    compliance_period = models.ForeignKey(
        CompliancePeriod,
        related_name='credit_trades',
        blank=True, null=True,
        on_delete=models.PROTECT
    )
    is_rescinded = models.BooleanField(
        default=False,
    )
    documents = ManyToManyField(
        'Document',
        through='DocumentCreditTrade'
    )

    class Meta:
        db_table = 'credit_trade'
