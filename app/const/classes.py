from aiogram.utils.callback_data import CallbackData


WishToDelete = CallbackData('delete', 'wish_id', 'hashed', 'is_reserved')
WishToReserve = CallbackData('reserve', 'wish_id', 'hashed')
WishToUnreserve = CallbackData('unreserve', 'wish_id', 'hashed')
AddLink = CallbackData('add_link', 'wish_id', 'hashed')
ToMyWishes = CallbackData('my_wishes')


class ProhibitedSymbols(BaseException):
    pass


class UserNotFound(BaseException):
    pass
