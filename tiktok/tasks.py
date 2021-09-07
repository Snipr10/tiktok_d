import concurrent
import logging
from concurrent.futures.thread import ThreadPoolExecutor
import datetime

import requests
from django.db.models import Q

from core.models import Sources, KeywordSource, Keyword, SourcesItems
from core.parsing_by_hashtag import parsing_hashtag
from core.parsing_by_username import parsing_username
from core.utils.utils import update_time_timezone
from core.celery import app
from django.utils import timezone

logger = logging.getLogger(__file__)

MAX_SIZE_PARSE_BY_WORD = 5
MAX_SIZE_PARSE_IN_CHANNEL = 4


@app.task
def start_task_webhook():
    requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7")


@app.task
def start_task_parsing_hashtags():
    pool_source = ThreadPoolExecutor(3)
    futures = []
    print("start_task_parsing_hashtags")
    select_sources = Sources.objects.filter(
        Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
        status=1)
    key_source = KeywordSource.objects.filter(source_id__in=list(select_sources.values_list('id', flat=True)))
    key_words = Keyword.objects.filter(network_id=9, enabled=1, taken=0,
                                       id__in=list(key_source.values_list('keyword_id', flat=True))
                                       ).order_by('last_modified')

    iteration = 0
    for key_word in key_words:
        try:
            if iteration > MAX_SIZE_PARSE_BY_WORD or \
                    Keyword.objects.filter(network_id=9, enabled=1, taken=1).count() > MAX_SIZE_PARSE_BY_WORD:
                break
            if key_word:
                select_source = select_sources.get(id=key_source.filter(keyword_id=key_word.id).first().source_id)
                last_update = key_word.last_modified
                time = select_source.sources
                if time is None:
                    time = 0
                if last_update is None or (last_update + datetime.timedelta(minutes=time) <
                                           update_time_timezone(timezone.localtime())):
                    try:
                        key_word.taken = 1
                        key_word.save(update_fields=["taken"])
                        futures.append(
                            pool_source.submit(parsing_hashtag, key_word))
                    except Exception as e:
                        print(e)
        except Exception:
            pass
        iteration += 1
        # TODO taken=0
    for future in concurrent.futures.as_completed(futures, timeout=1000):
        print(future.result())


@app.task
def start_task_parsing_accounts():
    print("start_task_parsing_accounts")
    requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?start_task_parsing_accounts")

    select_sources = Sources.objects.filter(
        Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
        status=1)
    # network_id
    all_sources_items = SourcesItems.objects.filter(network_id=9, disabled=0, taken=0,
                                                source_id__in=list(select_sources.values_list('id', flat=True)))
    null_sources_items = all_sources_items.filter(last_modified__isnull=True)
    if len(null_sources_items) > 0:
        sources_items = null_sources_items
    else:
        sources_items = all_sources_items

    pool_source = ThreadPoolExecutor(3)
    iteration = 0
    futures = []
    print(1)
    for sources_item in sources_items:
        print("sources_item")
        print(sources_item)
        requests.get(f"https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?sources_item={sources_item.id}")

        try:
            if iteration > MAX_SIZE_PARSE_IN_CHANNEL or \
                    SourcesItems.objects.filter(network_id=9, disabled=0, taken=1,
                                                source_id__in=list(select_sources.values_list('id', flat=True))
                                                ).count() > MAX_SIZE_PARSE_IN_CHANNEL:
                break
            print("time")

            time = select_sources.get(id=sources_item.source_id).sources
            if time is None:
                time = 0
            requests.get(f"https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?time={time}")

            if sources_item.last_modified is None or (
                    sources_item.last_modified + datetime.timedelta(minutes=time) <
                    update_time_timezone(timezone.localtime())):

                requests.get(f"https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?retro_date=")

                retro_date = select_sources.get(id=sources_item.source_id).retro
                last_update = sources_item.last_modified
                parsing_to = retro_date
                print("update_fields")

                try:
                    if not sources_item.foced and last_update is not None:
                        parsing_to = last_update.date()
                except Exception:
                    pass
                print("update_fields")

                result = False
                try:
                    print("update_fields")
                    sources_item.taken = 1
                    sources_item.save(update_fields=["taken"])
                    futures.append(
                        pool_source.submit(
                            parsing_username, sources_item, parsing_to
                        )
                    )

                except Exception as e:
                    print(e)
        except Exception:
            pass
        iteration += 1
        # TODO taken=0
    for future in concurrent.futures.as_completed(futures, timeout=1000):
        print(future.result())