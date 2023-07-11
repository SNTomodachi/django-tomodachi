#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations users
python manage.py makemigrations relationships
python manage.py makemigrations posts
python manage.py makemigrations reactions
python manage.py makemigrations comments
python manage.py migrate