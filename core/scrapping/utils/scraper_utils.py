import asyncio
import json
from datetime import datetime

from bs4 import BeautifulSoup


async def scroll_tiktok(count, page, body, attempt=0, parsing_to=None, round_scroll=0):
    while True:
        print("scroll_tiktok")
        print("round_scroll: " + str(round_scroll))
        if round_scroll > 30:
            break
        await asyncio.sleep(1)
        await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
        if count >= body.__len__():
            break
        else:
            count = body.__len__()
            attempt = 0
        round_scroll += 1

    # check data
    if parsing_to is not None and datetime.fromtimestamp(body[-1]['createTime']).date() < parsing_to:
        return

    if attempt < 2:
        await asyncio.sleep(5)
        await scroll_tiktok(count, page, body, attempt=attempt+1, round_scroll=round_scroll)
    return


async def get_headers(response, body, url):
    try:
        if url in response.url:
            text = await response.text()
            soup = BeautifulSoup(text)
            json_text = soup.find(id='__NEXT_DATA__').contents[0]
            data = json.loads(json_text)
            body += data['props']['pageProps']['items']
        if "https://m.tiktok.com/api/post/item_list" in response.url or "https://m.tiktok.com/api/challenge/item_list/"in response.url:
            try:
                items = await response.json()
                body += items['itemList']
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
