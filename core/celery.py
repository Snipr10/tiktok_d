import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiktok.settings')

import django

django.setup()

app = Celery('tiktok', include=['tiktok.tasks'])
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {

    'start_task_parsing_hashtags': {
        'task': 'tiktok.tasks.start_task_parsing_hashtags',
        'schedule': crontab(minute='*/10')
    },

    'start_task_parsing_accounts': {
        'task': 'tiktok.tasks.start_task_parsing_accounts',
        'schedule': crontab(minute='*/8')
    },
    'start_task_webhook': {
        'task': 'tiktok.tasks.start_task_webhook',
        'schedule': crontab(minute='*/50')
    },
    'stop_keys': {
        'task': 'tiktok.tasks.stop_keys',
        'schedule': crontab(minute='*/5')
    },
    'stop_channels': {
        'task': 'tiktok.tasks.stop_channels',
        'schedule': crontab(minute='*/5')
    },
}
