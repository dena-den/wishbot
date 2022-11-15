from aiogram import types
from app.const import classes


def start_menu_markup(is_user_exist: int):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if is_user_exist:
        markup.insert(types.KeyboardButton("Открыть мой список желаний"))
    else:
        markup.insert(types.KeyboardButton("Создать мой список желаний"))
    markup.insert(types.KeyboardButton("Выбрать подарок другу"))
    markup.insert(types.KeyboardButton("Забронированные мною подарки"))
    markup.insert(types.KeyboardButton("Разослать мой список друзьям"))
    markup.insert(types.KeyboardButton("Как со мной общаться?"))
    return markup


def back_to_markup(to: str):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if to == 'start':
        markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    elif to == 'name':
        markup.insert(types.KeyboardButton("Назад к вводу имени"))
    elif to == 'birthdate':
        markup.insert(types.KeyboardButton('Поделиться номером телефона',
                                           request_contact=True))
        markup.insert(types.KeyboardButton("Не хочу сообщать"))
        markup.insert(types.KeyboardButton("Назад к вводу даты рождения"))
    elif to == 'phone':
        markup.insert(types.KeyboardButton("Все правильно"))
        markup.insert(types.KeyboardButton("Назад к вводу телефона"))
    elif to == 'wishlist':
        markup.insert(types.KeyboardButton("Назад к списку"))
    return markup


def invitation_no_registered_user():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(types.KeyboardButton("Создать мой список желаний"))
    markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    return markup


def my_wishlist_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(types.KeyboardButton("Добавить желание"))
    markup.insert(types.KeyboardButton("Добавить желания списком"))
    markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    return markup


def delete_wish_button(wish_id: int,
                       hashed: int, 
                       delete_button_disabled: bool):
    markup = types.InlineKeyboardMarkup()
    if not delete_button_disabled:
        markup.add(types.InlineKeyboardButton(
            'Удалить',
            callback_data=classes.WishToDelete.new(
                wish_id=wish_id,
                hashed=hashed
            )
        ))
    markup.insert(types.InlineKeyboardButton(
                'Добавить ссылку',
                callback_data=classes.AddLink.new(
                    wish_id=wish_id,
                    hashed=hashed
                )
            ))
    return markup


def reserve_wish_button(wish_id: int, hashed: int):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Выбрать подарок',
        callback_data=classes.WishToReserve.new(
            wish_id=wish_id,
            hashed=hashed
        )
    ))
    return markup


def unreserve_wish_button(wish_id: int, hashed: int):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Отменить выбор',
        callback_data=classes.WishToUnreserve.new(
            wish_id=wish_id,
            hashed=hashed
        )
    ))
    return markup


def friend_wishlist_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    markup.insert(types.KeyboardButton("Назад к введению кода"))
    return markup

    
def wishes_reseved_by_me_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(types.KeyboardButton("Назад в стартовое меню"))
    markup.insert(types.KeyboardButton("Выбрать подарок другу"))
    return markup