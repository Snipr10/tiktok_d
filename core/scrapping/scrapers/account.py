import asyncio
from core.scrapping.models import AccountResult
from core.scrapping.scraper import BrowserManager, generate_cookie
from core.scrapping.utils.scraper_utils import get_headers, scroll_tiktok

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36'

NEW_PAGE_TIMEOUT = 60 * 1000
CAPTCHA_TIMEOUT = 1 * 1000


async def parsing_account(url, proxy):
    print(proxy)
    async with BrowserManager(proxy) as browser_manager:
        print("BrowserManager")

        browser = browser_manager.browser
        page = await browser.newPage()
        await page._client.send('Network.setCookies', {
            'cookies': generate_cookie(),
        })
        await page.authenticate({'username': proxy.login, 'password': proxy.proxy_password})

        await page.setUserAgent(USER_AGENT)
        body = []

        page.on("response",
                lambda req: asyncio.ensure_future(get_headers(req, body, url)))
        await page.goto(url)

        try:
            await page.waitForSelector("[role='dialog'", timeout=CAPTCHA_TIMEOUT)
            return AccountResult(success=False, captcha=True)
        except Exception:
            pass
        await scroll_tiktok(len(body), page, body, attempt=0)
        return AccountResult(body=body)
