from django.db import models

from tfrs.models.mixins.Auditable import Auditable


class Organization(Auditable):
    name = models.CharField(
        max_length=500
    )
    status = models.ForeignKey(
        'OrganizationStatus',
        related_name='organization_status',
        on_delete=models.PROTECT
    )
    actions_type = models.ForeignKey(
        'OrganizationActionsType',
        related_name='organization_actions_type',
        on_delete=models.PROTECT
    )
    type = models.ForeignKey(
        'OrganizationType',
        related_name='organization_type',
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'tfrs_organization'
