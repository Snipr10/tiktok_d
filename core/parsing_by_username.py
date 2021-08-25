import asyncio

from core.scrapping.scrapers.account import parsing_account
from core.utils.proxy import stop_proxy, get_proxy
from core.utils.save_json_to_db import save


def parsing_username(username, parsing_to=None):
    # TODO retro
    url = f"https://www.tiktok.com/@{username}"
    loop = asyncio.new_event_loop()
    proxy, proxy_data = get_proxy()
    if proxy is None:
        return None
    print("start")
    try:
        result = loop.run_until_complete(asyncio.wait_for(parsing_account(url, proxy_data, parsing_to), 300_000))
    except Exception as e:
        print(e)
        stop_proxy(proxy, banned=1)
        return False

    stop_proxy(proxy, result.captcha)
    save(result.body)

    if not result.success:
        return False
    return True
