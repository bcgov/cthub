from django.db import models

from tfrs.models.mixins.Auditable import Auditable
from .Organization import Organization


class User(Auditable):
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, verbose_name="username")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField()
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    cell_phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    _display_name = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        db_column="display_name",
    )
    organization = models.ForeignKey(
        Organization,
        related_name="users",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "tfrs_user"
