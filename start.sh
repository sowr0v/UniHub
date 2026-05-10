#!/usr/bin/env bash
set -o errexit

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Starting gunicorn..."
exec gunicorn unihub.wsgi:application --bind 0.0.0.0:${PORT:-10000} --log-file -
