import asyncio

from core.scrapping.scrapers.account import parsing_account
from core.utils.proxy import stop_proxy, get_proxy
from core.utils.save_json_to_db import save


def parsing_username(username):
    url = f"https://www.tiktok.com/@{username}"
    loop = asyncio.new_event_loop()
    proxy, proxy_data = get_proxy()
    if proxy is None:
        return None
    print("start")
    result = loop.run_until_complete(asyncio.wait_for(parsing_account(url, proxy_data), 30000))

    stop_proxy(proxy, result.captcha)

    if not result.success:
        return False

    save(result.body)

    return True
