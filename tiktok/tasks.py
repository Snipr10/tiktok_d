import logging
from datetime import timedelta

import requests
from django.db.models import Q

from tiktok.celery.celery import app
from django.utils import timezone

logger = logging.getLogger(__file__)


# @app.task
# def run_email():
#     try:
#         send_mail('GSM', 'HI, I am still working ', settings.EMAIL_HOST_USER, ['olegsh-gusev@mail.ru'])
#     except Exception as e:
#         print(str(e))


@app.task
def start_task_parsing_hashtags():
    print('start_task_new_sources')
