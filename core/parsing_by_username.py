import asyncio

from core.scrapping.scrapers.account import parsing_account
from core.utils.save_json_to_db import save


def parsing_username(username):
    url = f"https://www.tiktok.com/@{username}"
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(asyncio.wait_for(parsing_account(url), 30000))

    if not result.success:
        return False

    save(result.body)

    return True
