release: python manage.py migrate
web: gunicorn productimporter.wsgi --log-file –
worker: celery -A productimporter worker -l info