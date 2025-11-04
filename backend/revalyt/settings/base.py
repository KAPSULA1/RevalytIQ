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

import dj_database_url
import environ
from celery.schedules import crontab

# --------------------------------------------------------------
# Core paths and environment flags
# --------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    environ.Env.read_env(str(_env_file), overwrite=False)

ENVIRONMENT: str = env("ENVIRONMENT", default="local")
_legacy_debug = os.getenv("DEBUG")
_default_debug = (
    _legacy_debug.lower() == "true"
    if isinstance(_legacy_debug, str)
    else ENVIRONMENT != "production"
)
DEBUG: bool = env.bool("DJANGO_DEBUG", default=_default_debug)

SECRET_KEY: str = env("DJANGO_SECRET_KEY", default=os.getenv("SECRET_KEY", "django-insecure-key"))

_allowed_hosts_default = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1" if DEBUG else "revalyt.onrender.com",
)
ALLOWED_HOSTS: list[str] = [
    host.strip()
    for host in env("ALLOWED_HOSTS", default=_allowed_hosts_default).split(",")
    if host.strip()
]

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
_conn_age_raw = os.getenv("DB_CONN_MAX_AGE")
DB_CONN_MAX_AGE = env.int("DB_CONN_MAX_AGE", default=int(_conn_age_raw) if _conn_age_raw else 600)
_conn_health_raw = os.getenv("DB_CONN_HEALTH_CHECKS")
DB_CONN_HEALTH_CHECKS = env.bool(
    "DB_CONN_HEALTH_CHECKS",
    default=_conn_health_raw.lower() == "true"
    if isinstance(_conn_health_raw, str)
    else True,
)

DATABASE_URL = env("DATABASE_URL", default=os.getenv("DATABASE_URL", ""))
if DATABASE_URL:
    default_db = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=DB_CONN_MAX_AGE,
        conn_health_checks=DB_CONN_HEALTH_CHECKS,
    )
else:
    default_db = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_HOST", default=os.getenv("POSTGRES_HOST", "localhost")),
        "PORT": env("POSTGRES_PORT", default=os.getenv("POSTGRES_PORT", "5432")),
        "NAME": env("POSTGRES_DB", default=os.getenv("POSTGRES_DB", "revalytiq")),
        "USER": env("POSTGRES_USER", default=os.getenv("POSTGRES_USER", "revalytiq")),
        "PASSWORD": env("POSTGRES_PASSWORD", default=os.getenv("POSTGRES_PASSWORD", "password")),
        "CONN_MAX_AGE": DB_CONN_MAX_AGE,
        "CONN_HEALTH_CHECKS": DB_CONN_HEALTH_CHECKS,
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
    "PAGE_SIZE": env.int("API_PAGE_SIZE", default=50),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_LIFETIME", default=5)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_LIFETIME", default=7)),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_COOKIE": env("JWT_ACCESS_COOKIE_NAME", default="revalyt_access"),
    "AUTH_COOKIE_REFRESH": env("JWT_REFRESH_COOKIE_NAME", default="revalyt_refresh"),
    "AUTH_COOKIE_SECURE": env.bool("JWT_COOKIE_SECURE", default=not DEBUG),
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": env("JWT_COOKIE_PATH", default="/"),
    "AUTH_COOKIE_SAMESITE": env("JWT_COOKIE_SAMESITE", default="None"),
    "AUTH_COOKIE_DOMAIN": env("JWT_COOKIE_DOMAIN", default=None),
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
cors_origins_raw = env("CORS_ALLOWED_ORIGINS", default="")
default_frontend_origin = env("DEFAULT_FRONTEND_ORIGIN", default="http://localhost:3000")
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in cors_origins_raw.split(",")
    if origin.strip()
] or ([default_frontend_origin] if DEBUG else [])
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", default=True)

csrf_trusted_raw = env("CSRF_TRUSTED_ORIGINS", default="")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_trusted_raw.split(",")
    if origin.strip()
] or ([default_frontend_origin] if DEBUG else [])

# --------------------------------------------------------------
# Static / Media
# --------------------------------------------------------------
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = Path(
    env("STATIC_ROOT", default=os.getenv("STATIC_ROOT", str(BASE_DIR / "staticfiles")))
).resolve()
STATIC_ROOT.mkdir(parents=True, exist_ok=True)
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = Path(
    env("MEDIA_ROOT", default=os.getenv("MEDIA_ROOT", str(BASE_DIR / "media")))
).resolve()
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

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
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=CELERY_BROKER_URL)
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
TIME_ZONE = env("TIME_ZONE", default="UTC")
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
SECURE_REFERRER_POLICY = env("SECURE_REFERRER_POLICY", default="strict-origin-when-cross-origin")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="Lax" if DEBUG else "None")
CSRF_COOKIE_SAMESITE = env("CSRF_COOKIE_SAMESITE", default="Lax" if DEBUG else "None")
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0 if DEBUG else 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=not DEBUG)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=not DEBUG)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=not DEBUG)
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
