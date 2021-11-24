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
from django.db import models

from tfrs.managers.OrganizationManager import OrganizationManager
from auditable.models import Auditable


class TFRSOrganization(Auditable):
    """
    Contains a list of all of the recognized Part 3 fuel suppliers, both
    past and present, as well as an entry for the government which is also
    considered an organization.
    """
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
    objects = OrganizationManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tfrs_organization'

    db_table_comment = "Contains a list of all of the recognized Part 3 " \
                       "fuel suppliers, both past and present, as well as " \
                       "an entry for the government which is also " \
                       "considered an organization."
