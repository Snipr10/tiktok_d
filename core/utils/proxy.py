import datetime
import logging
import random
import time

from django.db.models import Q
from django.utils import timezone

from core.models import Proxy, AllProxy
from core.utils.utils import update_time_timezone

logger = logging.getLogger(__file__)


def get_proxy():
    try:
        print(1)
        time.sleep(random.randint(0, 10) / 10)
        added_proxy_list = list(Proxy.objects.all().values_list('id', flat=True))
        proxy = AllProxy.objects.filter(~Q(id__in=added_proxy_list), ~Q(port=0), ~Q(login='sergmga_gmail_com'),
                                        ~Q(login__contains='usr'),
                                        ~Q(login='sega364_pd_gmail_com'), ~Q(proxy_password='eTaYo7'), ip__isnull=False,
                                        login__isnull=False).last()
        print(2)

        if proxy is not None:
            new_proxy = Proxy.objects.create(id=proxy.id)
            return new_proxy, format_proxies(proxy)

        used_proxy = Proxy.objects.filter(banned=False, captcha=False,
                                          last_used__lte=update_time_timezone(
                                              timezone.localtime()
                                          ) - datetime.timedelta(minutes=5)).order_by('taken', 'last_used').first()
        print(3)

        if used_proxy is not None:
            used_proxy.taken = True
            used_proxy.save(update_fields=['taken'])
            proxies = get_proxies(used_proxy)
            if proxies is None:
                used_proxy.banned = True
                used_proxy.save(update_fields=['banned'])
                return get_proxy()
            else:
                return used_proxy, proxies
        return None, None
    except Exception as e:
        logger.error(e)
        return get_proxy()


def stop_proxy(proxy, captcha=0):
    proxy.captcha = captcha
    proxy.taken = 0
    proxy.last_used = update_time_timezone(timezone.localtime())
    proxy.save()


def get_proxies(proxy):
    proxy_info = AllProxy.objects.filter(id=proxy.id).first()
    if proxy_info is not None:
        # return format_proxies(proxy_info)
        return proxy_info
    return None


def format_proxies(proxy_info):

    return {'http': 'http://{}:{}@{}:{}'.format(proxy_info.login, proxy_info.proxy_password,proxy_info.ip,
                                                str(proxy_info.port)),
            'https': 'http://{}:{}@{}:{}'.format(proxy_info.login, proxy_info.proxy_password,proxy_info.ip,
                                                 str(proxy_info.port))
            }


def add_error(proxy):
    proxy.errors = proxy.errors + 1
    if proxy.errors > 10:
        proxy.banned = True
    proxy.taken = False
    proxy.last_used = update_time_timezone(timezone.localtime())
    proxy.save()
