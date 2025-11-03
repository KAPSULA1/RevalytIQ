from __future__ import annotations

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileUpdateSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Create a new user account."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes: list = []
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except ValidationError as exc:
            return Response(
                {"detail": "Validation error.", "errors": exc.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError:
            return Response(
                {
                    "detail": "Unable to create user.",
                    "errors": {
                        "non_field_errors": [
                            "A user with that username or email already exists."
                        ]
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {
                    "detail": "Unexpected error.",
                    "errors": {
                        "non_field_errors": [
                            "We could not complete your registration. Please try again."
                        ]
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = self.get_success_headers(serializer.data)
        data = serializer.data.copy()
        data.pop("password", None)
        data.pop("password2", None)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class MeView(generics.RetrieveAPIView):
    """Return authenticated user's info."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileView(generics.RetrieveUpdateAPIView):
    """Read/Update current user's profile (username/email)."""
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)


class ForgotPasswordView(APIView):
    """Accept email and (in DEBUG) return a demo token. In production just 200."""
    permission_classes = [permissions.AllowAny]
    authentication_classes: list = []

    def post(self, request):
        ser = ForgotPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        token_payload = {}
        user = User.objects.filter(email__iexact=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            if settings.DEBUG or os.environ.get("PYTEST_CURRENT_TEST"):
                token_payload = {"uid": uid, "token": token}
            # Integration point for email delivery can be added here.

        return Response(
            {
                "detail": "If an account exists for this email, you will receive further instructions.",
                **token_payload,
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    """Reset password using email+token (token checking is mocked for demo)."""
    permission_classes = [permissions.AllowAny]
    authentication_classes: list = []

    def post(self, request):
        ser = ResetPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]
        uidb64 = ser.validated_data["uid"]
        new_password = ser.validated_data["new_password"]
        token = ser.validated_data["token"]

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, email__iexact=email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Password reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Password reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
