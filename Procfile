release: python manage.py migrate
web: gunicorn fulfil_assignment.wsgi --log-file –
worker: celery -A productimporter -l info