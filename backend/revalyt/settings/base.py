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
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_LIFETIME", 5))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_LIFETIME", 7))),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------------------
# CORS configuration
# --------------------------------------------------------------
cors_origins_raw = os.getenv("CORS_ALLOWED_ORIGINS")
if cors_origins_raw:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]
else:
    CORS_ALLOW_ALL_ORIGINS = True

# --------------------------------------------------------------
# Static / Media
# --------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------------
# Celery / Redis
# --------------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

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
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
