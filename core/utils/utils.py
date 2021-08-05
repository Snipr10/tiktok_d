import datetime
import hashlib


def update_time_timezone(my_time):
    return my_time + datetime.timedelta(hours=3)


def get_sphinx_id(url):
    m = hashlib.md5()
    m.update(('https://t.me/{}'.format(url)).encode())
    return int(str(int(m.hexdigest(), 16))[:16])


def get_md5_text(text):
    if text is None:
        text = ''
    m = hashlib.md5()
    m.update(text.encode())
    return str(m.hexdigest())
