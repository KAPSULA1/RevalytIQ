from __future__ import annotations

from django.conf import settings
from django.db import connections
from django.http import JsonResponse
from redis import Redis
from redis.exceptions import RedisError

from .celery import app as celery_app


def _check_database() -> bool:
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception:
        return False


def _check_redis() -> bool:
    redis_url = getattr(settings, "REDIS_URL", None) or getattr(settings, "CELERY_BROKER_URL", None)
    if not redis_url:
        return False
    try:
        client = Redis.from_url(redis_url, socket_connect_timeout=1, socket_timeout=1)
        return bool(client.ping())
    except (RedisError, OSError):
        return False


def _check_celery() -> bool:
    try:
        inspection = celery_app.control.inspect(timeout=1.0)
        if not inspection:
            return False
        active = inspection.active()
        reserved = inspection.reserved()
        return bool(active or reserved or inspection.ping())
    except Exception:
        return False


def health(_request):
    db_ok = _check_database()
    redis_ok = _check_redis()
    celery_ok = _check_celery()

    status_code = 200 if all([db_ok, redis_ok, celery_ok]) else 503
    payload = {
        "status": "ok" if status_code == 200 else "degraded",
        "database": db_ok,
        "redis": redis_ok,
        "celery": celery_ok,
    }
    return JsonResponse(payload, status=status_code)
