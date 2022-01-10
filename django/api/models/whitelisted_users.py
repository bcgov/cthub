from django.db import models
from auditable.models import Auditable

class WhitelistedUsers(Auditable):
    user = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=100,
    )

    class Meta:
        db_table = 'whitelisted_users'
