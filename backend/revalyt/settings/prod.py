"""
Production settings for Render and other deployments.

Builds on :mod:`revalyt.settings.base` while enforcing hardened defaults suitable
for public environments.
"""

from __future__ import annotations

from .base import *  # noqa

ENVIRONMENT = "production"
DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS or ["revalyt.onrender.com"]

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="None")
CSRF_COOKIE_SAMESITE = env("CSRF_COOKIE_SAMESITE", default="None")
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

