"""
Base Django settings for RevalytIQ project.

Covers:
- PostgreSQL via DATABASE_URL (or discrete vars)
- JWT + DRF + CORS
- Celery + Redis
- Security hardening (auto when production)
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from celery.schedules import crontab

# --------------------------------------------------------------
# Core paths and environment flags
# --------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
_debug_override = os.getenv("DEBUG")
DEBUG: bool = (
    _debug_override.lower() == "true"
    if isinstance(_debug_override, str)
    else ENVIRONMENT != "production"
)

SECRET_KEY: str = os.getenv("SECRET_KEY", "django-insecure-key")

# Production host handling
ALLOWED_HOSTS: list[str] = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1" if DEBUG else "revalyt.onrender.com",
).split(",")

# --------------------------------------------------------------
# Installed apps
# --------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
    # Local apps
    "core",
    "analytics",
    "users",
]

# --------------------------------------------------------------
# Middleware
# --------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "revalyt.urls"
WSGI_APPLICATION = "revalyt.wsgi.application"

# --------------------------------------------------------------
# Templates
# --------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------------------
# Database
# --------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    scheme = (parsed.scheme or "").lower()
    if scheme in {"sqlite", "sqlite3"}:
        default_db = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": parsed.path or os.path.join(BASE_DIR, "db.sqlite3"),
        }
    else:
        default_db = {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": parsed.hostname or "localhost",
            "PORT": str(parsed.port or "5432"),
            "NAME": (parsed.path or "/revalytiq").lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
        }
else:
    default_db = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "NAME": os.getenv("POSTGRES_DB", "revalytiq"),
        "USER": os.getenv("POSTGRES_USER", "revalytiq"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
    }

DATABASES = {"default": default_db}

# --------------------------------------------------------------
# REST framework & JWT
# --------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "revalyt.authentication.CookieJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("API_PAGE_SIZE", 50)),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_LIFETIME", 5))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_LIFETIME", 7))),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_COOKIE": os.getenv("JWT_ACCESS_COOKIE_NAME", "revalyt_access"),
    "AUTH_COOKIE_REFRESH": os.getenv("JWT_REFRESH_COOKIE_NAME", "revalyt_refresh"),
    "AUTH_COOKIE_SECURE": os.getenv("JWT_COOKIE_SECURE", "False" if DEBUG else "True").lower() == "true",
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": os.getenv("JWT_COOKIE_PATH", "/"),
    "AUTH_COOKIE_SAMESITE": os.getenv("JWT_COOKIE_SAMESITE", "None"),
    "AUTH_COOKIE_DOMAIN": os.getenv("JWT_COOKIE_DOMAIN"),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "RevalytIQ API",
    "DESCRIPTION": "REST API powering the RevalytIQ analytics platform.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# --------------------------------------------------------------
# CORS configuration
# --------------------------------------------------------------
cors_origins_raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
default_frontend_origin = os.getenv("DEFAULT_FRONTEND_ORIGIN", "http://localhost:3000")
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in cors_origins_raw.split(",")
    if origin.strip()
] or ([default_frontend_origin] if DEBUG else [])
CORS_ALLOW_CREDENTIALS = True

csrf_trusted_raw = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_trusted_raw.split(",")
    if origin.strip()
] or ([default_frontend_origin] if DEBUG else [])

# --------------------------------------------------------------
# Static / Media
# --------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise configuration for efficient static file serving
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --------------------------------------------------------------
# Celery / Redis
# --------------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_BEAT_SCHEDULE = {
    "generate-daily-kpi": {
        "task": "analytics.tasks.generate_daily_report",
        "schedule": crontab(hour=0, minute=0),
        "options": {"expires": 3600},
    }
}

# --------------------------------------------------------------
# Timezone / Localization
# --------------------------------------------------------------
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
CELERY_TIMEZONE = TIME_ZONE
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------
# Password validation (secure defaults)
# --------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------
# Security (auto-activate in production)
# --------------------------------------------------------------
SECURE_REFERRER_POLICY = os.getenv("SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False" if DEBUG else "True").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False" if DEBUG else "True").lower() == "true"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax" if DEBUG else "None")
CSRF_COOKIE_SAMESITE = os.getenv("CSRF_COOKIE_SAMESITE", "Lax" if DEBUG else "None")
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
