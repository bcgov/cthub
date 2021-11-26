from django.db import models

from tfrs.models.mixins.Auditable import Auditable


class DocumentCreditTrade(Auditable):
    credit_trade = models.ForeignKey(
        'CreditTrade',
        on_delete=models.PROTECT
    )
    document = models.ForeignKey(
        'Document',
        on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'document_credit_trade'
        unique_together = (('credit_trade', 'document'),)
