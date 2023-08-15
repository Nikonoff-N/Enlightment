#!/bin/bash

echo "Waiting for postgres..."

sleep 5

echo "Apply database migrations"
python manage.py migrate


echo "Creating superuser"
python manage.py createsuperuser --noinput


echo "Starting server"
python manage.py runserver 0.0.0.0:8000
