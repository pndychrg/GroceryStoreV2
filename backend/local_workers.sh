#activating virutal env
. venv/bin/activate

celery -A run.celery worker -l info
deactivate