#activating virutal env
. venv/bin/activate

celery -A run.celery beat --max-interval 1 -l info
deactivate