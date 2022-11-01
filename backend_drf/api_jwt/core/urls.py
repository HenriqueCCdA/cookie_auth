from django.urls import path

from api_jwt.core.views import (
    MyLoginView,
    MyLogoutView,
    MyRefreshViewWithCookieSupport,
    get_user_info,
    register,
)

urlpatterns = [
    path('login', MyLoginView.as_view(), name='login'),
    path('token/logout', MyLogoutView.as_view(), name='logout'),
    path(
        'token/refresh',
        MyRefreshViewWithCookieSupport.as_view(),
        name='token_refresh',
    ),
    # path('users/<uuid:user_id>', get_user_info, name='get_user_info'),
    path('users/', get_user_info, name='get_user_info'),
    path('register', register, name='register'),
]
