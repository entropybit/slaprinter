__author__ = 'mithrawnuruodo'

from datetime import datetime

def now():
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return now


def now_unix():
    now = (datetime.now() - datetime(1970,1,1)).total_seconds()
    return int(now)
