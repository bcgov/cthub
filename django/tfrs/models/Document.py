from django.db.models import ManyToManyField


from tfrs.models.mixins.Auditable import Auditable
from tfrs.models.mixins.DocumentData import DocumentData


class Document(Auditable, DocumentData):
    credit_trades = ManyToManyField("CreditTrade", through="DocumentCreditTrade")

    class Meta:
        db_table = "document"
