"""
    REST API Documentation for the NRS TFRS Credit Trading Application

    The Transportation Fuels Reporting System is being designed to streamline
    compliance reporting for transportation fuel suppliers in accordance with
    the Renewable & Low Carbon Fuel Requirements Regulation.

    OpenAPI spec version: v1


    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from decimal import Decimal
from django.db import models
from django.db.models import ManyToManyField
from tfrs import validators

from auditable.models import Auditable

from .CompliancePeriod import CompliancePeriod
from .CreditTradeStatus import CreditTradeStatus
from .CreditTradeType import CreditTradeType
from .CreditTradeZeroReason import CreditTradeZeroReason
from .TFRSOrganization import TFRSOrganization


class CreditTrade(Auditable):
    """
    Holds the credit trade proposal information between the
    organizations
    """
    status = models.ForeignKey(
        CreditTradeStatus,
        related_name='credit_trades',
        on_delete=models.PROTECT
    )
    initiator = models.ForeignKey(
        TFRSOrganization,
        related_name='initiator_credit_trades',
        blank=True, null=True,
        on_delete=models.PROTECT
    )
    respondent = models.ForeignKey(
        TFRSOrganization,
        related_name='respondent_credit_trades',
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        CreditTradeType,
        related_name='credit_trades',
        on_delete=models.PROTECT)
    number_of_credits = models.IntegerField(
        validators=[validators.CreditTradeNumberOfCreditsValidator],
    )
    fair_market_value_per_credit = models.DecimalField(
        null=True, blank=True, max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[validators.CreditTradeFairMarketValueValidator],
    )
    zero_reason = models.ForeignKey(
        CreditTradeZeroReason,
        related_name='credit_trades',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    trade_effective_date = models.DateField(
        blank=True, null=True,
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

    db_table_comment = "Records all Credit Transfer Proposals, from " \
                       "creation to statutory decision to approved or decline."
