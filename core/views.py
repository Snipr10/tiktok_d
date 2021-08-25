import asyncio
import datetime

from django.shortcuts import render
import datetime
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Proxy
from core.parsing_by_hashtag import parsing_hashtag
from core.parsing_by_username import parsing_username
from core.scrapping.scrapers.hashtag import parsing_by_hashtag
from core.utils.proxy import stop_proxy, get_proxies
from core.utils.utils import update_time_timezone


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test_dava(request):
    # parsing_hashtag('test')
    s = False
    while s == False:
        s = parsing_username('dava_m', datetime.date.today())
    return Response("Ok")


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test_car(request):
    s = False
    while s == False:
        s = parsing_hashtag('s')
    return Response("Ok")

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test(request):
    url = f"https://www.tiktok.com/tag/spb"
    loop = asyncio.new_event_loop()
    proxy = Proxy.objects.filter(banned=False, captcha=False,
                                      last_used__lte=update_time_timezone(
                                          timezone.localtime()
                                      ) - datetime.timedelta(minutes=5)).order_by('taken', 'last_used').first()
    print(1)

    if proxy is not None:
        proxy.taken = True
        proxy.save(update_fields=['taken'])
        proxies = get_proxies(proxy)
    print(2)

    if proxy is None:
        return None
    print(3)

    try:
        result = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag(url, proxies), 30000))
    except Exception as e:
        print(e)
        stop_proxy(proxy, banned=1)
        return False
    stop_proxy(proxy, result.captcha)
    print(4)

    if not result.success:
        return False
    return Response("Ok")
