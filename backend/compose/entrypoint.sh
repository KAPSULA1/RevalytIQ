#!/bin/sh
set -euo pipefail

if [ -n "${DJANGO_SETTINGS_MODULE:-}" ]; then
  export DJANGO_SETTINGS_MODULE
else
  export DJANGO_SETTINGS_MODULE="revalyt.settings.base"
fi

python manage.py migrate --noinput

if [ "${DISABLE_COLLECTSTATIC:-0}" != "1" ]; then
  python manage.py collectstatic --noinput || true
fi

if [ "$#" -eq 0 ]; then
  set -- gunicorn revalyt.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-4}"
fi

exec "$@"
