from django.db import models

from auditable.models import Auditable


class Organization(Auditable):
    name = models.CharField(
        db_column="organization_name",
        max_length=500,
        null=False,
        unique=True
    )

    short_name = models.CharField(
        db_column='short_name',
        unique=True,
        null=True,
        max_length=64
    )

    is_active = models.BooleanField(
        default=False
    )
    is_government = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'organization'
