#!/usr/bin/env bash
set -o errexit

echo "=== Running database migrations ==="
python manage.py migrate --no-input

echo "=== Creating superuser if needed ==="
python manage.py ensure_superuser || echo "Warning: Could not create superuser"

echo "=== Starting gunicorn ==="
exec gunicorn unihub.wsgi:application --bind 0.0.0.0:${PORT:-10000} --log-file -
