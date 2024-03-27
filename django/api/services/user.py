from django.db import transaction
from api.models.user_permission import UserPermission
from api.models.permission import Permission
from api.models.user import User
from api.services.generic import get_objects_map


# this deletes all records in user_permission, and adds the new ones
@transaction.atomic
def update_permissions(user_permissions):
    permissions_map = get_objects_map(Permission.objects.all(), "description")
    users_map = get_objects_map(User.objects.all(), "idir")
    UserPermission.objects.all().delete()
    user_permissions_to_add = []
    for each in user_permissions:
        idir = each["idir"]
        permissions = each["user_permissions"]
        user = users_map.get(idir)
        permission_objects = []
        for description, value in permissions.items():
            if value == True:
                permission_objects.append(permissions_map.get(description))
        for permission_object in permission_objects:
            user_permissions_to_add.append(UserPermission(user=user, permission=permission_object))
    UserPermission.objects.bulk_create(user_permissions_to_add)
