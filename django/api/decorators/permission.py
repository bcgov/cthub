from rest_framework.response import Response
from rest_framework import status
from api.services.permissions import create_permission_list
from api.models.permission import Permission
from api.models.user import User
from api.models.user_permission import UserPermission


def check_upload_permission():
    def wrapper(func):
        def wrapped(request, *args, **kwargs):
            user = User.objects.filter(idir=request.user).first()
            user_permission = UserPermission.objects.filter(user_id=user.id)
            permissions = []
            if user_permission:
                for each in user_permission:
                    permission = Permission.objects.get(id=each.permission_id)
                    permissions.append(permission.description)
            if "uploader" not in permissions:
                return Response(
                    "You do not have permission to upload data.",
                    status=status.HTTP_403_FORBIDDEN,
                )
            return func(request, *args, **kwargs)

        return wrapped

    return wrapper


def check_admin_permission():
    def wrapper(func):
        def wrapped(request, *args, **kwargs):
            permissions = create_permission_list(request.user)
            if "admin" not in permissions:
                return Response(
                    "You do not have permission to make changes to other users' permissions.",
                    status=status.HTTP_403_FORBIDDEN,
                )
            return func(request, *args, **kwargs)

        return wrapped

    return wrapper
