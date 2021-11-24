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

from auditable.models import Auditable
from tfrs.managers.RoleManager import RoleManager


class Role(Auditable):
    """
    Table that will hold all the available Roles and descriptions
    """
    name = models.CharField(
        max_length=200,
        unique=True
    )

    description = models.CharField(
        max_length=1000
    )

    is_government_role = models.BooleanField(
        default=False
    )

    display_order = models.IntegerField()

    default_role = models.BooleanField(
        default=False
    )

    objects = RoleManager()

    def natural_key(self):
        """
        Allows us to match with the role name
        """
        return (self.name,)

    # Add effective_date and expiration_date
    class Meta:
        db_table = 'role'

    db_table_comment = "Table that will hold all the available Roles " \
                       "and descriptions."
