#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r myenv/requirements.txt

cd myenv/ecomproject 

python manage.py collectstatic --no-input
python manage.py migrate