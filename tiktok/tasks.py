import logging
from datetime import timedelta
import datetime

import requests
from django.db.models import Q

from core.models import Sources, KeywordSource, Keyword, SourcesItems
from core.parsing_by_hashtag import parsing_hashtag
from core.parsing_by_username import parsing_username
from core.utils.utils import update_time_timezone
from tiktok.celery.celery import app
from django.utils import timezone

logger = logging.getLogger(__file__)


@app.task
def start_task_parsing_hashtags():
    print("start_task_parsing_hashtags")
    select_sources = Sources.objects.filter(
        Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
        status=1)
    print("1")

    key_source = KeywordSource.objects.filter(source_id__in=list(select_sources.values_list('id', flat=True)))

    print("2")

    key_word = Keyword.objects.filter(network_id=9, enabled=1, taken=0,
                                      id__in=list(key_source.values_list('keyword_id', flat=True))
                                      ).order_by('last_modified').last()
    print("3")
    print("key_word" + str(key_word))
    if key_word:
        select_source = select_sources.get(id=key_source.filter(keyword_id=key_word.id).first().source_id)
        print("4")

        last_update = key_word.last_modified
        time = select_source.sources
        if time is None:
            time = 0
        if last_update is None or (last_update + datetime.timedelta(minutes=time) <
                                   update_time_timezone(timezone.localtime())):
            result = False
            try:
                key_word.taken = 1
                key_word.save()
                attempt = 0
                while not result and attempt < 10:
                    print("key_word start_task_parsing_hashtags")
                    result = parsing_hashtag(key_word.keyword)
                    attempt += 1
            except Exception as e:
                pass
            key_word.taken = 0
            if result:
                key_word.last_modified = update_time_timezone(timezone.localtime())
            key_word.save()


@app.task
def start_task_parsing_accounts():
    print("start_task_parsing_accounts")

    select_sources = Sources.objects.filter(
        Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
        status=1)
    # network_id
    print(1)
    sources_item = SourcesItems.objects.filter(network_id=8, disabled=0, taken=0,
                                               source_id__in=list(select_sources.values_list('id', flat=True))) \
        .order_by('last_modified').last()
    print(2)

    if sources_item:
        time = select_sources.get(id=sources_item.source_id).sources
        print(3)

        if time is None:
            time = 0
        if sources_item.last_modified is None or (
                sources_item.last_modified + datetime.timedelta(minutes=time) <
                update_time_timezone(timezone.localtime())):
            print(4)

            retro_date = select_sources.get(id=sources_item.source_id).retro
            last_update = sources_item.last_modified
            parsing_to = retro_date
            try:
                if not sources_item.foced and last_update is not None:
                    parsing_to = last_update.date()
            except Exception:
                pass
            result = False
            try:
                sources_item.taken = 1
                sources_item.save()
                attempt = 0
                while not result and attempt < 10:
                    print("parsing_username start_task_parsing_accounts")

                    result = parsing_username(sources_item.data, parsing_to)
                    attempt += 1
            except Exception as e:
                print(e)
            if result:

                sources_item.last_modified = update_time_timezone(timezone.localtime())

            sources_item.taken = 0
            sources_item.save()
