import asyncio

import requests

from core.scrapping.models import AccountResult
from core.scrapping.scraper import BrowserManager, generate_cookie
from core.scrapping.utils.scraper_utils import get_headers, scroll_tiktok

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36'

NEW_PAGE_TIMEOUT = 60 * 1000
CAPTCHA_TIMEOUT = 1 * 1000


async def parsing_account(url, proxy, parsing_to):
    print(proxy)
    requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?parsing_account=")

    async with BrowserManager(proxy) as browser_manager:
        print("BrowserManager")

        browser = browser_manager.browser
        page = await browser.newPage()
        await page._client.send('Network.setCookies', {
            'cookies': generate_cookie(),
        })
        print("authenticate")

        await page.authenticate({'username': proxy.login, 'password': proxy.proxy_password})
        print("USER_AGENT")

        await page.setUserAgent(USER_AGENT)
        body = []
        print("response")

        page.on("response",
                lambda req: asyncio.ensure_future(get_headers(req, body, url)))
        print(url)
        await page.goto(url)

        try:
            await page.waitForSelector("[role='dialog'", timeout=CAPTCHA_TIMEOUT)
            return AccountResult(success=False, captcha=True)
        except Exception:
            pass
        print("NOT CAPTHCA")
        if len(body) ==0:
            # BAD Res
            print("body 0")
            return AccountResult(body=body)
        try:
            print("scroll_tiktok 0")

            await scroll_tiktok(len(body), page, body, attempt=0, parsing_to=parsing_to)
        except Exception as e:
            print(e)
        print(body)

        return AccountResult(body=body)
