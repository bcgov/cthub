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
from django.contrib.auth.models import AbstractUser
import django.contrib.auth.validators

from auditable.models import Auditable
from tfrs.managers.UserManager import UserManager


class User(AbstractUser, Auditable):
    """
    User Model
    """
    username = models.CharField(
        error_messages={'unique': "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters, digits and "
                  "@/./+/-/_ only.",
        max_length=150, unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        verbose_name='username'
    )

    password = models.CharField(
        max_length=128, blank=True, null=True)
    email = models.EmailField(
        blank=True, null=True)

    title = models.CharField(
        max_length=100, blank=True, null=True)
    phone = models.CharField(
        max_length=50, blank=True, null=True,
        )
    cell_phone = models.CharField(
        max_length=50, blank=True, null=True,
        )
    organization = models.ForeignKey(
        'TFRSOrganization', related_name='users', blank=True, null=True,
        on_delete=models.SET_NULL)

    _display_name = models.CharField(
        max_length=500, blank=True, null=True, db_column='display_name',
        )

    def __str__(self):
        return str(self.id)

    objects = UserManager()

    def natural_key(self):
        return (self.username,)

    class Meta:
        db_table = 'user'

    # Supplemental mapping for base class
    db_column_supplemental_comments = {
        'first_name': 'Django field. First name (retrieved from Siteminder',
        'last_name': 'Django field. Last name (retrieved from Siteminder)',
        'is_staff': 'Django field. Flag. True if staff user.',
        'is_superuser': 'Django field. Flag. True if superuser.',
        'is_active': 'Django field. True if can login.',
        'date_joined': 'Django field. Date account created.',
        'last_login': 'Django field. Last login time.',
    }

    db_table_comment = 'Users who may access the application'
