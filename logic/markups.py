from aiogram import types
from const import classes
from logic import utils


def start_menu_markup(is_user_exist: int):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if is_user_exist:
        markup.insert(types.KeyboardButton("Открыть мой список подарков"))
    else:
        markup.insert(types.KeyboardButton("Создать мой список подарков"))
    markup.insert(types.KeyboardButton("Выбрать подарок другу"))
    return markup


def back_to_markup(to: str):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if to == 'start':
        markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    elif to == 'name':
        markup.insert(types.KeyboardButton("Назад к вводу имени"))
    elif to == 'birthdate':
        markup.insert(types.KeyboardButton("Не хочу сообщать"))
        markup.insert(types.KeyboardButton("Назад к вводу даты рождения"))
    elif to == 'phone':
        markup.insert(types.KeyboardButton("Все правильно"))
        markup.insert(types.KeyboardButton("Назад к вводу телефона"))
    elif to == 'wishlist':
        markup.insert(types.KeyboardButton("Назад к списку"))
    return markup


def my_wishlist_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(types.KeyboardButton("Добавить подарок"))
    markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    return markup


def delete_wish_button(id: int, name: str):
    markup = types.InlineKeyboardMarkup()
    gift_data = dict(id=id, name=name)
    markup.add(types.InlineKeyboardButton('Удалить', callback_data=utils.pack_json(gift_data)))
    return markup