import asyncio

import requests

from core.scrapping.models import AccountResult
from core.scrapping.scraper import BrowserManager
from core.scrapping.utils.scraper_utils import get_headers, scroll_tiktok

NEW_PAGE_TIMEOUT = 60 * 1000
CAPTCHA_TIMEOUT = 1 * 1000
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

CHROME_REVISION = '884014'


async def parsing_by_hashtag(url, proxy):
    requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?url_parsing_by_hashtag")

    async with BrowserManager(proxy) as browser_manager:
        requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?BrowserManager")

        browser = browser_manager.browser
        print("browser")

        page = await browser.newPage()
        print("page")
        requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?page")

        await page.evaluateOnNewDocument(
            """() => {
            delete navigator.__proto__.webdriver;
            }"""
        )
        print("evaluateOnNewDocument")

        await page.setUserAgent(USER_AGENT)
        print("setUserAgent")

        await page.authenticate({'username': proxy.login, 'password': proxy.proxy_password})
        print("authenticate")
        requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?authenticate")
        requests.get(f"https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?{proxy.login}")

        body = []

        page.on("response",
                lambda req: asyncio.ensure_future(get_headers(req, body, url)))
        print(url)
        await page.goto(url, timeout=60_000)
        print("page.goto")
        requests.get("https://webhook.site/32acbe47-1d04-479f-9759-8ea9c87d5cd7?page_goto")

        # page_content = await page.content()
        # if "Хэштег не найден" in page_content:
        #     return AccountResult(not_founded=True)
        try:
            await page.waitForSelector("[role='dialog'", timeout=CAPTCHA_TIMEOUT)
            print("captcha")
            return AccountResult(success=False, captcha=True)
        except Exception:
            pass
        if len(body) == 0:
            # BAD Res
            print("BAD captcha")
            return AccountResult(body=body)

            # return AccountResult(success=False, captcha=True)
        try:
            await scroll_tiktok(len(body), page, body, attempt=0)
        except Exception as e:
            print(e)
        print("len body" + str(body))
        # cookies = await get_cookies(page)
        return AccountResult(body=body)
