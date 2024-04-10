from django.db import models
from auditable.models import Auditable


class UserPermission(Auditable):
    user = models.ForeignKey("User", related_name="user", on_delete=models.CASCADE)
    permission = models.ForeignKey(
        "Permission", related_name="permission", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_permission"

    db_table_comment = "Contains the relationship between user and permission tables "
