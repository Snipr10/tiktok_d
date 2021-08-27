import asyncio

from core.scrapping.scrapers.hashtag import parsing_by_hashtag
from core.utils.proxy import get_proxy, stop_proxy
from core.utils.save_json_to_db import save


def parsing_hashtag(hashtag):
    url = f"https://www.tiktok.com/tag/{hashtag}"
    loop = asyncio.new_event_loop()
    proxy, proxy_data = get_proxy()
    if proxy is None:
        return None
    try:
        result = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag(url, proxy_data), 10_000_000))
    except Exception as e:
        print(e)
        stop_proxy(proxy, banned=1)
        return False
    stop_proxy(proxy, result.captcha)
    if not result.success:
        return False

    save(result.body)

    return True
