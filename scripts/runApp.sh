#!/usr/bin/env bash

scripts/wait-for-it.sh db:5432 -t 30
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python preConfig.py
python manage.py runserver 0.0.0.0:8000
