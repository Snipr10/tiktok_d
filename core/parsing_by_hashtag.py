import asyncio

from core.scrapping.scrapers.hashtag import parsing_by_hashtag
from core.utils.proxy import get_proxy, stop_proxy
from core.utils.save_json_to_db import save
from core.utils.utils import update_time_timezone
from django.utils import timezone


def parsing_hashtag(key_word):
    url = f"https://www.tiktok.com/tag/{key_word.keyword.replace(' ', '')}"
    loop = asyncio.new_event_loop()
    proxy, proxy_data = get_proxy()
    if proxy is None:
        key_word.taken = 1
        key_word.save(update_fields=["taken"])
        return None
    is_success = True
    try:
        result = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag(url, proxy_data), 10_000_000))
    except Exception as e:
        print(e)
        stop_proxy(proxy, banned=1)
        is_success = False
    stop_proxy(proxy, result.captcha)
    if not result.success:
        is_success = False
    try:
        save(result.body)
    except Exception:
        is_success = False

    key_word.taken = 1

    if is_success:
        key_word.last_modified = update_time_timezone(timezone.localtime())
        key_word.save(update_fields=["taken", "last_modified"])
    else:
        key_word.save(update_fields=["taken"])
    return result
