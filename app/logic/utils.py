from pytz import timezone
from datetime import datetime
from random import randint
import re
from app.const import classes


class Dict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__getitem__


def get_moscow_datetime():
    spb_timezone = timezone("Europe/Moscow")
    local_time = datetime.now().replace(microsecond=0)
    current_time = local_time.astimezone(spb_timezone)
    return current_time


def birthdate_processing(input: str):
    prohibited_symbols = r'[a-zA-ZёЁа-яА-Я]'
    if re.search(prohibited_symbols, input):
        return False
    numbers_pattern = r'[0-9]'
    birthdate_numbers = ''.join(re.findall(numbers_pattern, input))
    if len(birthdate_numbers) != 8:
        return False
    try:
        birthdate = datetime.strptime(birthdate_numbers, r'%d%m%Y').date()
    except ValueError:
        return False
    return birthdate


def code_processing(input: str):
    prohibited_symbols = r'[a-zA-ZёЁа-яА-Я]'
    if re.search(prohibited_symbols, input):
        raise classes.ProhibitedSymbols
    numbers_pattern = r'[0-9]'
    code_numbers = ''.join(re.findall(numbers_pattern, input))
    return code_numbers
