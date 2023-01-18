from aiogram.dispatcher.filters.state import State, StatesGroup


class Wish(StatesGroup):
    wish_name_to_add = State()
    wish_names_to_add = State()
    wish_link_to_add = State()


class Friend(StatesGroup):
    friend_code = State()

class Admin(StatesGroup):
    mailing_text = State()
