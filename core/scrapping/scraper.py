import logging
import os
import random
import requests

from pyppeteer import launch

from core.scrapping.utils.chromium import revert_to_original_chromium_version

logger = logging.getLogger(__name__)

FINDING_ERROR_MESSAGES_TIMEOUT = 2 * 1000
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3419.0 Safari/537.36'


class BrowserManager:

    def __init__(self, proxy, chromium_version=None, **kargs):
        self.browser = None
        self.proxy = proxy
        self.params = kargs

        # default chromium version for pyppeteer==0.2.5 is 588429 (see pyppeteer.__chromium_revision__)
        # For other available versions, see https://github.com/puppeteer/puppeteer#q-which-chromium-version-does-puppeteer-use
        # self.chromium_version = chromium_version

    async def __aenter__(self):
        # set_chromium_version(self.chromium_version)

        headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        print('-proxy-server')
        print(  f'--proxy-server={self.proxy.ip}:{self.proxy.port}')
        self.browser = await launch(headless=headless,
                                    handleSIGINT=False,
                                    handleSIGTERM=False,
                                    handleSIGHUP=False,
                                    args=[
                                        "--no-sandbox",
                                        f'--proxy-server={self.proxy.ip}:{self.proxy.port}'
                                    ])
        # await page.authenticate({'username': 'KWE18Q', 'password': 'y08j96'})
        return self

    async def __aexit__(self, type, value, traceback):
        if self.browser:
            await self.browser.close()
            revert_to_original_chromium_version()


def to_curl(req):
    command = "curl --location --request {method} '{uri}'\\\n"
    command += "  --header {headers}"
    method = req.method
    uri = req.url
    data = req.body
    headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
    headers = "\\\n  --header ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)


async def get_cookies(page):
    return await page._client.send('Network.getAllCookies')


def cookies_to_session(cookies, headers={}):
    session = requests.session()
    cookies_jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies:
        cookies_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

    session.cookies = cookies_jar
    session.headers.update(headers)

    return session


def cookies_jar_to_array(cookies_jar):
    cookies = []
    for cookie_jar in cookies_jar:
        cookie = {}
        for name in ("version", "name", "value",
                     "port", "port_specified",
                     "domain", "domain_specified", "domain_initial_dot",
                     "path", "path_specified",
                     "secure", "expires", "discard", "comment", "comment_url",
                     ):
            attr = getattr(cookie_jar, name)
            cookie.update({name: attr})
        cookies.append(cookie)
    return cookies


def generate_cookie():
    return [
        {
            'name': 'tt_webid_v2',
            'value': str(random.randint(10000, 999999999)),
            'domain': '.tiktok.com',
            'path': '/',
            'expires': -1,
            'size': 49,
            'httpOnly': False,
            'secure': True,
            'session': True
        },
        {
            'name': 's_v_web_id',
            'value': 'verify_khgp4f49_V12d4mRX_MdCO_4Wzt_Ar0k_z4RCQC9pUDpX',
            'domain': '.tiktok.com',
            'path': '/',
            'expires': -1,
            'size': 49,
            'httpOnly': False,
            'secure': True,
            'session': True
        }

    ]


async def get_page(browser):
    page = await browser.newPage()
    # await page._client.send('Network.setCookies', {
    #     'cookies': generate_cookie(),
    # })
    await page.evaluateOnNewDocument(
        """() => {
        delete navigator.__proto__.webdriver;
        }"""
    )
    await page.setUserAgent(USER_AGENT)

    return page
