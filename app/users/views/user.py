from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core import response
from ..serializers.user import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.filter(is_active=True)
        role = self.request.query_params.get("role")
        q = self.request.query_params.get("q")
        if role:
            qs = qs.filter(role=role)
        if q:
            qs = qs.filter(username__icontains=q)
        return qs

    def list(self, request):
        """Get all active users"""
        qs = self.get_queryset()
        serializer = UserSerializer(qs, many=True)
        return response.Ok(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Created(serializer.data)

    def update(self, request, pk=None):
        """Update user with given pk"""
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Ok(serializer.data)

    def destroy(self, request, pk=None):
        """Update user with given pk"""
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.is_active = False
        instance.delete()
        return response.NoContent()


class CurrentUserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request):
        """Get logged in user profile"""
        serializer = UserSerializer(self.get_object())
        return response.Ok(serializer.data)

    @action(detail=False, methods=['put'])
    def put(self, request):
        """Update logged in user profile"""
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Ok(serializer.data)
