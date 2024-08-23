#!/bin/bash

# Check the command passed to the container
if [ "$1" = 'web' ]; then
    # Start Django development server
    python manage.py runserver 0.0.0.0:8000
elif [ "$1" = 'celery' ]; then
    # Start Celery worker
    celery -A pdfparser worker --loglevel=info
else
    # Run the command provided in CMD
    exec "$@"
fi
