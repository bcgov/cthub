from rest_framework import exceptions
from api.models.whitelisted_users import WhitelistedUsers

def check_whitelist():
    def wrapper(func):
        def wrapped(request, *args, **kwargs):
            user = request.user
            whitelisted_users = WhitelistedUsers.objects.filter(user=user)
            if not whitelisted_users:
                raise exceptions.PermissionDenied(
                    'You do not have permission to upload data.'
                )
            return func(request, *args, **kwargs)
        return wrapped
    return wrapper
