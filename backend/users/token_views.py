from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def _cookie_settings(expires: timedelta):
    cfg = settings.SIMPLE_JWT
    return {
        "max_age": int(expires.total_seconds()),
        "secure": cfg.get("AUTH_COOKIE_SECURE", not settings.DEBUG),
        "httponly": cfg.get("AUTH_COOKIE_HTTP_ONLY", True),
        "samesite": cfg.get("AUTH_COOKIE_SAMESITE", "None"),
        "domain": cfg.get("AUTH_COOKIE_DOMAIN"),
        "path": cfg.get("AUTH_COOKIE_PATH", "/"),
    }


def _set_auth_cookies(response: Response, access: str, refresh: str) -> None:
    cfg = settings.SIMPLE_JWT
    access_cookie = cfg.get("AUTH_COOKIE")
    refresh_cookie = cfg.get("AUTH_COOKIE_REFRESH")
    if access_cookie and access:
        response.set_cookie(
            access_cookie,
            access,
            **_cookie_settings(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]),
        )
    if refresh_cookie and refresh:
        response.set_cookie(
            refresh_cookie,
            refresh,
            **_cookie_settings(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]),
        )


def _clear_auth_cookies(response: Response) -> None:
    cfg = settings.SIMPLE_JWT
    cookie_kwargs = {
        "secure": cfg.get("AUTH_COOKIE_SECURE", not settings.DEBUG),
        "httponly": cfg.get("AUTH_COOKIE_HTTP_ONLY", True),
        "samesite": cfg.get("AUTH_COOKIE_SAMESITE", "None"),
        "domain": cfg.get("AUTH_COOKIE_DOMAIN"),
        "path": cfg.get("AUTH_COOKIE_PATH", "/"),
    }
    for cookie_name in (cfg.get("AUTH_COOKIE"), cfg.get("AUTH_COOKIE_REFRESH")):
        if cookie_name:
            response.delete_cookie(cookie_name, **cookie_kwargs)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Issue JWT pair and persist them in httpOnly cookies.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])

        data = serializer.validated_data
        response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, data.get("access"), data.get("refresh"))
        return response


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
        _set_auth_cookies(response, data.get("access"), data.get("refresh", refresh_token))
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
        _clear_auth_cookies(response)
        return response
