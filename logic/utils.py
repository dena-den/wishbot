import json
from pytz import timezone
import datetime
from random import randint


class Dict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__getitem__


def pack_json(data):
    return json.dumps(data)


def unpack_json(callback_data):
    return json.loads(callback_data)


def get_moscow_datetime():
    spb_timezone = timezone("Europe/Moscow")
    local_time = datetime.datetime.now().replace(microsecond=0)
    current_time = local_time.astimezone(spb_timezone)
    return current_time
