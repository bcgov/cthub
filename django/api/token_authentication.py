from rest_framework.authentication import TokenAuthentication
from api.models.app_user import AppToken


class CustomTokenAuthentication(TokenAuthentication):
    model = AppToken
