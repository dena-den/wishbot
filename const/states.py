from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    name = State()
    birthdate = State()
    phone = State()


class Wish(StatesGroup):
    wish_name_to_add = State()
    wish_name_to_del = State()

class Friend(StatesGroup):
    friend_code = State()
