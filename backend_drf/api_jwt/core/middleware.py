from dj_rest_auth.jwt_auth import JWTCookieAuthentication, set_jwt_access_cookie
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class SimpleMiddleware(JWTCookieAuthentication):
    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response
        self.new_access_token = False
        super().__init__(*args, **kwargs)

    def __call__(self, request):

        try:
            user, validated_token = self.authenticate(request)

            request.user = user

        except InvalidToken:
            pass
            # return response(data={'Refresh Token invalido.'}, status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)

        if self.new_access_token:
            set_jwt_access_cookie(response, validated_token)
            self.new_access_token = False

        return response

    def authenticate(self, request):
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        raw_access_token = request.COOKIES.get(cookie_name)

        if raw_access_token is None:
            raw_access_token = self.new_raw_access_token(request)
            self.new_access_token = True

        validated_token = self.get_validated_token(raw_access_token)

        user = self.get_user(validated_token)

        return user, validated_token

    def new_raw_access_token(self, request):

        cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
        if cookie_name and cookie_name in request.COOKIES:
            token = request.COOKIES.get(cookie_name)
            serializer = TokenRefreshSerializer()
            data = serializer.validate({'refresh': token})
            return data['access']
        else:
            from rest_framework_simplejwt.exceptions import InvalidToken

            raise InvalidToken('No valid refresh token found.')
