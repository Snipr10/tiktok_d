import concurrent
import logging
from concurrent.futures.thread import ThreadPoolExecutor
import datetime

from django.db.models import Q

from core.models import Sources, KeywordSource, Keyword, SourcesItems
from core.parsing_by_hashtag import parsing_hashtag
from core.parsing_by_username import parsing_username
from core.utils.utils import update_time_timezone
from tiktok.celery.celery import app
from django.utils import timezone

logger = logging.getLogger(__file__)

MAX_SIZE_PARSE_BY_WORD = 5


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
                    Keyword.objects.filter(network_id=8, enabled=1, taken=1).count() > MAX_SIZE_PARSE_BY_WORD:
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

    select_sources = Sources.objects.filter(
        Q(retro_max__isnull=True) | Q(retro_max__gte=timezone.now()), published=1,
        status=1)
    # network_id
    sources_items = SourcesItems.objects.filter(network_id=9, disabled=0, taken=0,
                                                source_id__in=list(select_sources.values_list('id', flat=True)))
    null_sources_items = sources_items.filter(last_modified__isnull=True)
    if len(null_sources_items) > 0:
        sources_item = null_sources_items.first()
    else:
        sources_item = sources_items.order_by('last_modified').first()
    print(sources_item)
    if sources_item:
        time = select_sources.get(id=sources_item.source_id).sources
        if time is None:
            time = 0
        if sources_item.last_modified is None or (
                sources_item.last_modified + datetime.timedelta(minutes=time) <
                update_time_timezone(timezone.localtime())):

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
                    result = parsing_username(sources_item.data, parsing_to)

                    attempt += 1
            except Exception as e:
                print(e)
            if result:
                sources_item.last_modified = update_time_timezone(timezone.localtime())
                sources_item.save(update_fields=["taken", "last_modified"])
            else:
                sources_item.save(update_fields=["taken"])
