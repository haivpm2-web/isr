#!/usr/bin/env bash
set -euo pipefail

python3 manage.py collectstatic --noinput || python manage.py collectstatic --noinput
python3 manage.py migrate || python manage.py migrate
python3 manage.py seed_demo_data || python manage.py seed_demo_data

exec python3 -m gunicorn hospital_isr.wsgi --bind 0.0.0.0:${PORT:-8000}