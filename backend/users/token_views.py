from __future__ import annotations

from datetime import timedelta
from typing import Optional
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from publicsuffix2 import get_sld
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def _normalize_host(raw_value: Optional[str]) -> Optional[str]:
    if not raw_value:
        return None
    value = raw_value.strip()
    if "," in value:
        value = value.split(",", 1)[0]
    if not value:
        return None
    if "://" in value:
        parsed = urlparse(value)
        host = parsed.hostname
    else:
        host = value
    if not host:
        return None
    cleaned = host.split("/", 1)[0].split(":", 1)[0].strip().lower().strip(".")
    if cleaned.startswith("[") and cleaned.endswith("]"):  # IPv6 literals.
        cleaned = cleaned[1:-1]
    return cleaned or None


def _effective_host(request: HttpRequest) -> Optional[str]:
    forwarded_host = request.META.get("HTTP_X_FORWARDED_HOST")
    candidates = [
        forwarded_host,
        request.get_host(),
        request.META.get("HTTP_HOST"),
        request.META.get("HTTP_ORIGIN"),
        request.META.get("HTTP_REFERER"),
    ]
    for candidate in candidates:
        normalized = _normalize_host(candidate)
        if normalized:
            return normalized
    return None


def _normalized_allowed_hosts() -> set[str]:
    allowed = set()
    for entry in settings.ALLOWED_HOSTS:
        value = (entry or "").strip()
        if not value or value == "*":
            continue
        allowed.add(value.lstrip(".").lower())
    return allowed


def _cookie_domain(request: HttpRequest) -> Optional[str]:
    configured = settings.SIMPLE_JWT.get("AUTH_COOKIE_DOMAIN")
    if configured:
        return configured

    host = _effective_host(request)
    if not host:
        return None

    if "." not in host:
        return None

    if all(part.isdigit() for part in host.split(".")):
        return None

    registrable = get_sld(host)
    if (
        registrable
        and registrable != host
        and registrable in _normalized_allowed_hosts()
    ):
        return registrable

    return host


def _cookie_settings(expires: timedelta, request: Optional[HttpRequest] = None):
    cfg = settings.SIMPLE_JWT
    domain = cfg.get("AUTH_COOKIE_DOMAIN")
    if domain is None and request is not None:
        domain = _cookie_domain(request)
    return {
        "max_age": int(expires.total_seconds()),
        "secure": cfg.get("AUTH_COOKIE_SECURE", not settings.DEBUG),
        "httponly": cfg.get("AUTH_COOKIE_HTTP_ONLY", True),
        "samesite": cfg.get("AUTH_COOKIE_SAMESITE", "None"),
        "domain": domain,
        "path": cfg.get("AUTH_COOKIE_PATH", "/"),
    }


def _set_auth_cookies(
    response: Response,
    request: HttpRequest,
    access: str,
    refresh: str,
) -> None:
    cfg = settings.SIMPLE_JWT
    access_cookie = cfg.get("AUTH_COOKIE")
    refresh_cookie = cfg.get("AUTH_COOKIE_REFRESH")
    if access_cookie and access:
        response.set_cookie(
            access_cookie,
            access,
            **_cookie_settings(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"], request),
        )
    if refresh_cookie and refresh:
        response.set_cookie(
            refresh_cookie,
            refresh,
            **_cookie_settings(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"], request),
        )


def _clear_auth_cookies(response: Response, request: HttpRequest) -> None:
    cfg = settings.SIMPLE_JWT
    cookie_kwargs = {
        "secure": cfg.get("AUTH_COOKIE_SECURE", not settings.DEBUG),
        "httponly": cfg.get("AUTH_COOKIE_HTTP_ONLY", True),
        "samesite": cfg.get("AUTH_COOKIE_SAMESITE", "None"),
        "domain": _cookie_domain(request),
        "path": cfg.get("AUTH_COOKIE_PATH", "/"),
    }
    for cookie_name in (cfg.get("AUTH_COOKIE"), cfg.get("AUTH_COOKIE_REFRESH")):
        if cookie_name:
            response.delete_cookie(cookie_name, **cookie_kwargs)


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    """
    Allow logging in with either the username or e-mail address.
    """

    def validate(self, attrs):
        attrs = attrs.copy()
        username_input = attrs.get(self.username_field)

        if username_input and "@" in username_input:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=username_input)
            except ObjectDoesNotExist:
                pass
            else:
                attrs[self.username_field] = getattr(user, self.username_field)

        return super().validate(attrs)


@method_decorator(csrf_exempt, name='dispatch')
class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Issue JWT pair and persist them in httpOnly cookies.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = EmailOrUsernameTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])

        data = serializer.validated_data
        response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, request, data.get("access"), data.get("refresh"))
        return response


@method_decorator(csrf_exempt, name='dispatch')
class CookieTokenRefreshView(TokenRefreshView):
    """
    Rotate refresh tokens stored in cookies.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_cookie = settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH")
        provided_refresh = request.data.get("refresh")
        refresh_token = provided_refresh or (request.COOKIES.get(refresh_cookie) if refresh_cookie else None)

        if refresh_token is None:
            raise InvalidToken("Refresh token is missing.")

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])

        data = serializer.validated_data
        response = Response({"detail": "Token refreshed."}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, request, data.get("access"), data.get("refresh", refresh_token))
        return response


class CookieTokenLogoutView(APIView):
    """
    Blacklist refresh token and clear cookies.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_cookie = settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH")
        refresh_token = request.COOKIES.get(refresh_cookie) if refresh_cookie else None
        response = Response({"detail": "Logged out."}, status=status.HTTP_205_RESET_CONTENT)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass
        _clear_auth_cookies(response, request)
        return response
