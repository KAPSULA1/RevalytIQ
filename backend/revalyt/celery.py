from __future__ import annotations

import os

from celery import Celery

settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "revalyt.settings.prod")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("revalyt")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
