from keycloak import KeycloakOpenID

from django.conf import settings
from rest_framework import authentication, exceptions


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)

        if not auth:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        try:
            scheme, token = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        if not token:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            realm_name=settings.KEYCLOAK_REALM
        )

        # Decode the token from the front-end
        KEYCLOAK_PUBLIC_KEY = \
            "-----BEGIN PUBLIC KEY-----\n" + \
            keycloak_openid.public_key() + \
            "\n-----END PUBLIC KEY-----"

        options = {
            'verify_signature': True,
            'verify_aud': True,
            'verify_exp': True
        }

        token_info = keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options=options
        )

        # Get the user from the keycloak server based on the token
        print(
            "identity_provider: {identity_provider}, idir_username: {idir_username}, email: {email}, preferred_username: {preferred_username}".format(
                identity_provider=token_info.get(
                    "identity_provider", "no identity_provider"
                ),
                idir_username=token_info.get("idir_username", "no idir_username"),
                email=token_info.get("email", "no email"),
                preferred_username=token_info.get(
                    "preferred_username", "no preferred_username"
                ),
            )
        )

        user_info = keycloak_openid.userinfo(token)
        if user_info.get('user_id') != token_info.get('user_id'):
            raise exceptions.AuthenticationFailed(
                'Invalid Token'
            )
        return user_info.get('idir_username'), None

        # user = None
    #     if 'user_id' not in user_info:
    #         # try email
    #         if 'email' in user_info:
    #             user_profile = UserProfile.objects.filter(
    #                 keycloak_email__iexact=user_info.get('email')
    #             )

    #             if not user_profile.exists():
    #                 raise exceptions.AuthenticationFailed(
    #                     "User does not exist.")

    #             if user_profile.count() > 1:
    #                 preferred_username, _ = user_info.get(
    #                     'preferred_username').split('@')

    #                 user_profile = user_profile.filter(
    #                     username__iexact=preferred_username
    #                 )

    #             user = user_profile.first()
    #         else:
    #             raise exceptions.AuthenticationFailed(
    #                 'user_id or email is required in jwt payload')
    #     else:
    #         try:
    #             user = UserProfile.objects.get_by_natural_key(
    #                 user_info.get('user_id')
    #             )
    #         except UserProfile.DoesNotExist:
    #             raise exceptions.AuthenticationFailed(
    #                 'user_id "{}" does not exist'.format(
    #                     user_info.get('user_id')
    #                 ))

    #     if not user.is_active:
    #         raise exceptions.PermissionDenied(
    #             'Your account is currently inactive. Please contact your '
    #             'administrator to re-activate your account.'
    #         )

    #     return user, None
