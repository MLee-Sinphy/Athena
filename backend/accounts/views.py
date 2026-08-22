from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .authentication import issue_token, revoke_user_tokens
from .permissions import AdministratorOnly, PasswordChanged
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    ReaderCreateSerializer,
)

INVALID_CREDENTIALS = {"detail": "Invalid identifier or password."}
DUMMY_PASSWORD_HASH = make_password("a timing-only password value")


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data["identifier"]
        users = get_user_model().objects.filter(
            Q(email__iexact=identifier)
            | Q(registration_id=identifier)
            | Q(whatsapp_number=identifier)
        )
        if role := serializer.validated_data.get("role"):
            users = users.filter(role=role)
        user = users.first()
        password_hash = user.password if user else DUMMY_PASSWORD_HASH
        password_valid = check_password(serializer.validated_data["password"], password_hash)
        if not user or not user.is_active or not password_valid:
            return Response(INVALID_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            {
                "access_token": issue_token(user),
                "token_type": "Bearer",
                "must_change_password": user.must_change_password,
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.utils import timezone

        request.auth.revoked_at = timezone.now()
        request.auth.save(update_fields=["revoked_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["current_password"]):
            return Response({"current_password": ["Incorrect password."]}, status=400)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.must_change_password = False
        request.user.save(update_fields=["password", "must_change_password", "updated_at"])
        revoke_user_tokens(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request, user_id):
        target = get_object_or_404(get_user_model(), pk=user_id)
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target.set_password(serializer.validated_data["temporary_password"])
        target.must_change_password = True
        target.save(update_fields=["password", "must_change_password", "updated_at"])
        revoke_user_tokens(target)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReaderCreateView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = ReaderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
