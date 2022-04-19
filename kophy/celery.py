import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kophy.settings')

app = Celery('main')

app.conf.enable_utc=True

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# sauce codes: 245074

#it will search the app module for task.py, import it then run any function with @shared_task decorator
app.autodiscover_tasks(['app'])



# sauce codes: 165684