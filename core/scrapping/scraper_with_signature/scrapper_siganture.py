
BASE_URL = "https://m.tiktok.com/"


def __init__(self, **kwargs):
    """The TikTokApi class. Used to interact with TikTok.
    :param logging_level: The logging level you want the program to run at
    :param request_delay: The amount of time to wait before making a request.
    :param executablePath: The location of the chromedriver.exe
    """
    self.debug = kwargs.get("debug", False)
    self.signer_url = kwargs.get("external_signer", None)
    self.proxy = kwargs.get("proxy", None)
    if self.debug:
        print("Class initialized")
    self.executablePath = kwargs.get("executablePath", None)

    self.userAgent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/86.0.4240.111 Safari/537.36"
    )

    # Get Browser Params
    b = browser("newParam", newParams=True, **kwargs)

    try:
        self.timezone_name = self.__format_new_params__(b.timezone_name)
        self.browser_language = self.__format_new_params__(b.browser_language)
        self.browser_platform = self.__format_new_params__(b.browser_platform)
        self.browser_name = self.__format_new_params__(b.browser_name)
        self.browser_version = self.__format_new_params__(b.browser_version)
        self.width = b.width
        self.height = b.height
    except Exception as e:
        if self.debug:
            print("The following error occurred, but it was ignored.")
            print(e)

        self.timezone_name = ""
        self.browser_language = ""
        self.browser_platform = ""
        self.browser_name = ""
        self.browser_version = ""
        self.width = "1920"
        self.height = "1080"

    self.request_delay = kwargs.get("request_delay", None)


def external_signer(self, url, custom_did=None):
    if custom_did != None:
        query = {
            "url": url,
            "custom_did": custom_did
        }
    else:
        query = {
            "url": url,
        }
    data = requests.get(self.signer_url + "?{}".format(urlencode(query)))
    parsed_data = data.json()

    return parsed_data['verifyFp'], parsed_data['did'], parsed_data['_signature'], parsed_data['userAgent'], \
           parsed_data['referrer']


def getData(self, b, **kwargs) -> dict:
    """Returns a dictionary of a response from TikTok.
    :param api_url: the base string without a signature
    :param b: The browser object that contains the signature
    :param language: The two digit language code to make requests to TikTok with.
                     Note: This doesn't seem to actually change things from the API.
    :param proxy: The IP address of a proxy server to request from.
    """
    (
        region,
        language,
        proxy,
        maxCount,
        did,
    ) = self.__process_kwargs__(kwargs)
    kwargs['custom_did'] = did
    if self.request_delay is not None:
        time.sleep(self.request_delay)

    if self.proxy != None:
        proxy = self.proxy

    if self.signer_url == None:
        userAgent = b.userAgent
        referrer = b.referrer
    else:
        verify_fp, did, signature, userAgent, referrer = self.external_signer(kwargs['url'],
                                                                              custom_did=kwargs.get('custom_did', None))
    query = {"verifyFp": b.verifyFp, "did": b.did, "_signature": b.signature}
    url = "{}&{}".format(b.url, urlencode(query))
    r = requests.get(
        url,
        headers={
            "authority": "m.tiktok.com",
            "method": "GET",
            "path": url.split("tiktok.com")[1],
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "referer": referrer,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": userAgent,
            "cookie": "tt_webid_v2=" + did + ';s_v_web_id=' + kwargs.get("custom_verifyFp",
                                                                         "verify_khgp4f49_V12d4mRX_MdCO_4Wzt_Ar0k_z4RCQC9pUDpX"),
        },
        proxies=self.__format_proxy(proxy),
    )
    try:
        return r.json()
    except Exception as e:
        logging.error(e)
        logging.error(
            "Converting response to JSON failed response is below (probably empty)"
        )
        logging.info(r.text)
        raise Exception("Invalid Response")


def getBytes(self, b, **kwargs) -> bytes:
    """Returns bytes of a response from TikTok.
    :param api_url: the base string without a signature
    :param b: The browser object that contains the signature
    :param language: The two digit language code to make requests to TikTok with.
                     Note: This doesn't seem to actually change things from the API.
    :param proxy: The IP address of a proxy server to request from.
    """
    (
        region,
        language,
        proxy,
        maxCount,
        did,
    ) = self.__process_kwargs__(kwargs)
    kwargs['custom_did'] = did
    if self.signer_url == None:
        userAgent = b.userAgent
        referrer = b.referrer
    else:
        verify_fp, did, signature, userAgent, referrer = self.external_signer(kwargs['url'],
                                                                              custom_did=kwargs.get('custom_did', None))
    query = {"verifyFp": b.verifyFp, "did": b.did, "_signature": b.signature}
    url = "{}&{}".format(b.url, urlencode(query))
    r = requests.get(
        url,
        headers={
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Accept-Language": "en-US;en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "cookie": "tt_webid_v2=" + did,
            "Host": url.split("/")[2],
            "Pragma": "no-cache",
            "Range": "bytes=0-",
            "Referer": "https://www.tiktok.com/",
            "User-Agent": userAgent,
        },
        proxies=self.__format_proxy(proxy),
    )
    return r.content


def trending(self, count=30, minCursor=0, maxCursor=0, **kwargs) -> dict:
    """
    Gets trending TikToks
    """
    (
        region,
        language,
        proxy,
        maxCount,
        did,
    ) = self.__process_kwargs__(kwargs)
    kwargs['custom_did'] = did

    response = []
    first = True

    while len(response) < count:
        if count < maxCount:
            realCount = count
        else:
            realCount = maxCount

        query = {
            "count": realCount,
            "id": 1,
            "secUid": "",
            "maxCursor": maxCursor,
            "minCursor": minCursor,
            "sourceType": 12,
            "appId": 1233,
            "region": region,
            "priority_region": region,
            "language": language,
        }
        api_url = "{}api/item_list/?{}&{}".format(
            BASE_URL, self.__add_new_params__(), urlencode(query)
        )
        b = browser(api_url, **kwargs)
        res = self.getData(b, **kwargs)

        for t in res.get("items", []):
            response.append(t)

        if not res["hasMore"] and not first:
            logging.info("TikTok isn't sending more TikToks beyond this point.")
            return response[:count]

        realCount = count - len(response)
        maxCursor = res["maxCursor"]

        first = False

    return response[:count]