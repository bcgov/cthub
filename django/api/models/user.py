from django.db import models
from auditable.models import Auditable


class User(Auditable):
    idir = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=100,
    )

    class Meta:
        db_table = "user"

    db_table_comment = "Contains the list of users in the system "
