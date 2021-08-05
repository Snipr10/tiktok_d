import asyncio

from core.scrapping.scrapers.hashtag import parsing_by_hashtag
from core.utils.save_json_to_db import save


def parsing_hashtag(hashtag):
    url = f"https://www.tiktok.com/tag/{hashtag}"
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag(url), 30000))

    if not result.success:
        return False

    save(result.body)

    return True
