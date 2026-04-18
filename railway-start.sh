#!/usr/bin/env bash
set -euo pipefail

/opt/venv/bin/python manage.py collectstatic --noinput
/opt/venv/bin/python manage.py migrate
/opt/venv/bin/python manage.py seed_demo_data

exec /opt/venv/bin/python -m gunicorn hospital_isr.wsgi --bind 0.0.0.0:${PORT:-8000}