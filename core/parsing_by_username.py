import asyncio

import requests

from core.scrapping.scrapers.account import parsing_account
from core.utils.proxy import stop_proxy, get_proxy
from core.utils.save_json_to_db import save
from core.utils.utils import update_time_timezone
from django.utils import timezone


def parsing_username(sources_item, parsing_to=None):
    url = f"https://www.tiktok.com/@{sources_item.data}"

    loop = asyncio.new_event_loop()
    proxy, proxy_data = get_proxy()
    if proxy is None:
        sources_item.taken = 0
        sources_item.save(update_fields=["taken"])
        return None
    print("start")
    is_success = True
    result = None
    try:
        result = loop.run_until_complete(asyncio.wait_for(parsing_account(url, proxy_data, parsing_to), 300_000))
    except Exception as e:
        print(e)
        is_success = False
        stop_proxy(proxy, banned=1)
    if not result.success:
        is_success = False
    stop_proxy(proxy, result.captcha)
    try:
        save(result.body)
    except Exception:
        is_success = False

    sources_item.taken = 0
    if is_success:
        sources_item.last_modified = update_time_timezone(timezone.localtime())
        sources_item.save(update_fields=["taken", "last_modified"])
    else:
        sources_item.save(update_fields=["taken"])
    return result

