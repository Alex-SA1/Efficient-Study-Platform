#!/bin/bash

# Load environment variables from .env if exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python manage.py migrate
python manage.py collectstatic --noinput

# Run Daphne for Django Channels
daphne -b 0.0.0.0 -p 8000 efficient_study_platform.asgi:application
