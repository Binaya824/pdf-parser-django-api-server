from __future__ import absolute_import , unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'pdfparser.settings')

app = Celery('pdfparser')

app.config_from_object('django.conf:settings' , namespace='CELERY')

# Set worker concurrency to 1 to ensure tasks are processed one by one
app.conf.worker_concurrency = 1

# Optional: Set the task_acks_late to True if you want tasks to be acknowledged after they are fully processed
app.conf.task_acks_late = True

# Optional: Use a custom queue if needed
app.conf.task_default_queue = 'default'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))