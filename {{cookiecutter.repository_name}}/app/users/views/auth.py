from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core import response
from ..serializers.auth import ChangePasswordSerializer, LoginSerializer
from ..serializers.user import UserSerializer

User = get_user_model()


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            raise ValidationError("Please provide both username and password")
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError("Invalid Credentials")
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        data = serializer.data.copy()
        data['token'] = token.key
        return response.Ok(data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("old_password")):
                raise ValidationError("Wrong Password")

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return response.Ok({"success": "Successfully Changed."})

        return response.BadRequest(serializer.errors)
