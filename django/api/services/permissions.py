from api.models.user import User
from api.models.user_permission import UserPermission
from api.models.permission import Permission


def create_permission_list(user):
    user = User.objects.filter(idir=user).first()
    user_permission = UserPermission.objects.filter(user_id=user.id)
    permissions = []
    if user_permission:
        for each in user_permission:
            permission = Permission.objects.get(id=each.permission_id)
            permissions.append(permission.description)
    return permissions


def get_permissions_map(users):
    result = {}
    user_permissions = UserPermission.objects.select_related(
        "user", "permission"
    ).filter(user__in=users)
    for each in user_permissions:
        user = each.user
        permission = each.permission
        if not user in result:
            result[user] = []
        result[user].append(permission)
    return result


def get_permissions_representation(permissions):
    result = {}
    if permissions is not None:
        for permission in permissions:
            result[permission.description] = True
    return result
