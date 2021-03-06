#!/bin/bash
python manage.py makemigrations
python manage.py migrate
gunicorn --reload -w 4 -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8000 config.asgi:application