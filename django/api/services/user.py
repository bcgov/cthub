from api.models.user_permission import UserPermission
from api.models.permission import Permission
from api.models.user import User

def update_permissions(self, request):
    msg = []
    permissions = Permission.objects.all()
    UserPermission.objects.all().delete()
    for each in request.data:
        for k, v in each.items():
            if k == 'idir':
                user = User.objects.get(idir=v)
            if k == 'user_permissions':
                for permission_description, value in v.items():
                    if value == True or (user.idir == request.user and permission_description == 'admin'):
                    ## if they are updating permissions then they are already admin user, they cannot remove their own admin
                        permission = permissions.get(description=permission_description)
                        try:
                            UserPermission.objects.create(user_id=user.id, permission_id=permission.id)
                        except Exception as error:
                            msg.append("{} permission could not be added to {}".format(permission_description, user.idir))