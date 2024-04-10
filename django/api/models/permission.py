from django.db import models
from auditable.models import Auditable


class Permission(Auditable):
    description = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=100,
    )

    class Meta:
        db_table = "permission"

    db_table_comment = (
        "Contains the list of permissions to grant access to "
        "certain actions of areas for the system."
    )
