from django.urls import path, include
from rest_framework import routers

from .views import auth
from .views import user

router = routers.DefaultRouter()
router.register(r'me', user.CurrentUserViewSet, basename="me")
router.register(r'users', user.UserViewSet, basename="users")

urlpatterns = [
    path('users/', include(router.urls)),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('change-password/',
         auth.ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),
]
