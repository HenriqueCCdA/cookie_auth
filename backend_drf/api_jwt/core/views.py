from dj_rest_auth.jwt_auth import (
    CookieTokenRefreshSerializer,
    set_jwt_access_cookie,
    set_jwt_cookies,
    set_jwt_refresh_cookie,
    unset_jwt_cookies,
)
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from api_jwt.core.auth import MyJWTCookieAuthentication
from api_jwt.core.serializers import RegisterSerializer

AUTH_HEADER_TYPES = jwt_settings.AUTH_HEADER_TYPES


User = get_user_model()


@api_view(['GET'])
@authentication_classes([MyJWTCookieAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request, user_id):
    user = request.user
    return Response({'uuid': user.uuid, 'email': user.email, 'name': user.name})


@api_view(['POST'])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.create(serializer.validated_data)

    access_token, refresh_token = jwt_encode(user)

    user_info = RegisterSerializer(instance=user)

    response = Response(data=user_info.data, status=status.HTTP_201_CREATED)

    set_jwt_cookies(response, access_token, refresh_token)
    return response


class MyLoginView(LoginView):
    def get_response(self):

        data = {'uuid': self.user.uuid, 'message': 'Login success'}

        response = Response(data, status=status.HTTP_200_OK)
        set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response


class MyLogoutView(LogoutView):
    def logout(self, request):

        response = Response({'detail': _('Successfully logged out.')}, status=status.HTTP_200_OK)

        if getattr(settings, 'REST_USE_JWT', False):

            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)

            if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(request.COOKIES[refresh_cookie_name])
                    token.blacklist()
                except KeyError:
                    response.data = {'detail': _('Refresh cookie was not included in request.')}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                    return response
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, 'args'):
                        if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                            response.data = {'detail': _(error.args[0])}
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {'detail': _('An error has occurred.')}
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {'detail': _('An error has occurred.')}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                    return response

            elif not cookie_name:
                message = _(
                    'Neither cookies or blacklist are enabled, so the token '
                    'has not been deleted server side. Please make sure the token is deleted client side.',
                )
                response.data = {'detail': message}
                response.status_code = status.HTTP_200_OK

            unset_jwt_cookies(response)

        return response


class MyRefreshViewWithCookieSupport(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200 and 'access' in response.data:
            set_jwt_access_cookie(response, response.data['access'])
            if not settings.JWT_AUTH_IN_BODY:
                response.data.pop('access')
            response.data['access_token_expiration'] = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        if response.status_code == 200 and 'refresh' in response.data:
            set_jwt_refresh_cookie(response, response.data['refresh'])
            if not settings.JWT_AUTH_IN_BODY:
                response.data.pop('refresh')
            response.data['refrash_token_expiration'] = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME

        return super().finalize_response(request, response, *args, **kwargs)
