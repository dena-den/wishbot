from aiogram import types
from app.const import classes


def start_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Открыть мой вишлист",
        callback_data=classes.MyWishlist.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Выбрать подарок другу",
        callback_data=classes.FindFriend.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Забронированные подарки",
        callback_data=classes.ReservedWishes.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Поделиться вишлистом",
        callback_data=classes.Invitation.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Как со мной общаться?",
        callback_data=classes.Instruction.new())
    )
    return markup


def back_to_start_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Главное меню",
        callback_data=classes.Start.new())
    )
    return markup


def back_to_my_wishlist_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Назад в мой вишлист",
        callback_data=classes.MyWishlist.new())
    )
    return markup


def create_my_wishlist_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Создать мой вишлист",
        callback_data=classes.MyWishlist.new())
    )
    return markup


def my_wishlist_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)   
    markup.insert(types.InlineKeyboardButton(
        "Добавить желание",
        callback_data=classes.AddWish.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Добавить желания списком",
        callback_data=classes.AddWishes.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Главное меню",
        callback_data=classes.Start.new())
    )
    return markup


def delete_wish_button(
    wish_id: int,
    hashed: int, 
    is_wish_reserved: bool
):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(
        'Удалить',
        callback_data=classes.WishToDelete.new(
            wish_id=wish_id,
            hashed=hashed,
            is_reserved=is_wish_reserved,
            message_to_delete=''
        )
    ))
    markup.insert(types.InlineKeyboardButton(
        'Добавить описание',
        callback_data=classes.AddLink.new(
            wish_id=wish_id,
            hashed=hashed
        )
    ))
    return markup


def deleting_approval_button(wish_id: int, hashed: int, message_to_delete: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(
        'Да, удаляй',
        callback_data=classes.WishToDelete.new(
            wish_id=wish_id,
            hashed=hashed,
            is_reserved=False,
            message_to_delete=message_to_delete
        )
    ))
    markup.insert(types.InlineKeyboardButton(
        'Назад к списку',
        callback_data=classes.MyWishlist.new()
    ))
    return markup


def reserve_wish_button(wish_id: int, hashed: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(
        'Выбрать подарок',
        callback_data=classes.WishToReserve.new(
            wish_id=wish_id,
            hashed=hashed
        )
    ))
    return markup


def unreserve_wish_button(wish_id: int, hashed: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(
        'Отменить выбор',
        callback_data=classes.WishToUnreserve.new(
            wish_id=wish_id,
            hashed=hashed
        )
    ))
    return markup


def friend_wishlist_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Другой вишлист",
        callback_data=classes.FindFriend.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Главное меню",
        callback_data=classes.Start.new())
    )
    return markup

    
def wishes_reseved_by_me_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(
        "Выбрать вишлист друга",
        callback_data=classes.FindFriend.new())
    )
    markup.insert(types.InlineKeyboardButton(
        "Главное меню",
        callback_data=classes.Start.new())
    )
    return markup


def last_viewed_friends_markup(last_viewed_data):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for user_data in last_viewed_data:
        friend_user_id = user_data.pop('friend_user_id')
        full_user_name = ' '.join(filter(lambda data: data, user_data.values()))
        markup.insert(types.InlineKeyboardButton(
            full_user_name,
            callback_data=classes.LastViewedId.new(
                friend_user_id=friend_user_id
            )
        ))
    if len(last_viewed_data) % 2 == 1:
        markup.insert(types.InlineKeyboardButton(
            '❌',
            callback_data=classes.EmptyCallback.new()
        )) 
    markup.add(types.InlineKeyboardButton(
        'Назад в стартовое меню',
        callback_data=classes.Start.new()
    ))
    return markup
