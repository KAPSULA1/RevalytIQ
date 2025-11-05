"""
Demo settings for the Render free-tier deployment.

This profile keeps production hardening but runs Celery synchronously and
avoids external services such as Redis so the app works on a single dyno.
"""

from __future__ import annotations

from .prod import *  # noqa: F401,F403

ENVIRONMENT = "demo"

# Celery runs synchronously; no Redis required.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "memory://")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "cache+memory://")

# Use in-memory cache/sessions for the demo.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "revalytiq-demo",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Flag used by seed_demo management command.
ENABLE_DEMO_SEED = os.getenv("ENABLE_DEMO_SEED", "true").lower() == "true"
