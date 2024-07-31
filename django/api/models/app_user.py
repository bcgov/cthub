from django.db import models
from auditable.models import Auditable
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class AppUser(Auditable):
    is_active = models.BooleanField(default=True)

    app_name = models.CharField(max_length=100, unique=True)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        db_table = "app_user"

    db_table_comment = (
        "represents an external application that integrates this app via API"
    )


class AppToken(Token):
    user = models.OneToOneField(
        AppUser,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )

    class Meta:
        db_table = "app_token"

    db_table_comment = (
        "the token of an external application that integrates this app via API"
    )
