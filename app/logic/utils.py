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

# not used
def birthdate_processing(input: str):
    prohibited_symbols = r'[a-zA-ZёЁа-яА-Я]'
    if re.search(prohibited_symbols, input):
        return False
    numbers_pattern = r'[0-9]'
    birthdate_numbers = ''.join(re.findall(numbers_pattern, input))
    try:
        if len(birthdate_numbers) == 8:
            birthdate = datetime.strptime(birthdate_numbers, r'%d%m%Y').date()
            return birthdate   
        elif len(birthdate_numbers) == 4:
            birthdate_numbers = f'{birthdate_numbers}1000'
            birthdate = datetime.strptime(birthdate_numbers, r'%d%m%Y').date()
            return birthdate
        else:
            return False
    except ValueError:
        return False

# not used
def format_birthdate(input):
    if input.year == 1000:
        birthdate = input.strftime('%d.%m')
    else:
        birthdate = input.strftime('%d.%m.%Y')
    return birthdate


def code_processing(input: str):
    code_pattern = r'[0-9]{6}'
    is_valid = re.fullmatch(code_pattern, input)
    if is_valid:
        return int(input)
    else:
        raise classes.CodeNotValid
