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