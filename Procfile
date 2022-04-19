release: python3 manage.py migrate
web: gunicorn kophy.wsgi --log-file -
worker: celery -A kophy worker -l info -B