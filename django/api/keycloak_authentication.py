from keycloak import KeycloakOpenID
from django.conf import settings
from rest_framework import authentication, exceptions
from api.models.user import User


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", None)
        if settings.KEYCLOAK_TESTING:
            try:
                user = User.objects.get(idir=auth['idir'])
                return user.idir, None
            except User.DoesNotExist as exc:
                # print("Testing User does not exist")
                raise User.DoesNotExist(str(exc))
        if not auth:
            raise exceptions.AuthenticationFailed("Authorization token required")
        try:
            scheme, token = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed("Authorization token required")

        if not token:
            raise exceptions.AuthenticationFailed("Authorization token required")

        keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            realm_name=settings.KEYCLOAK_REALM,
        )

        token_info = keycloak_openid.decode_token(token, True, check_claims={"aud": settings.KEYCLOAK_CLIENT_ID, "exp": None})
        if token_info.get("identity_provider") != "idir":
            raise exceptions.AuthenticationFailed("Invalid Token")
        return token_info.get("idir_username"), None
