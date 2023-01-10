from aiogram.utils.callback_data import CallbackData


WishToDelete = CallbackData('delete', 'wish_id', 'hashed', 'is_reserved')
WishToReserve = CallbackData('reserve', 'wish_id', 'hashed')
WishToUnreserve = CallbackData('unreserve', 'wish_id', 'hashed')
AddLink = CallbackData('add_link', 'wish_id', 'hashed')
ToMyWishes = CallbackData('my_wishes')
ToStart = CallbackData('start')
LastViewedId = CallbackData('last_viewed', 'friend_user_id')
EmptyCallback = CallbackData('empty')


class ProhibitedSymbols(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserIsYou(BaseException):
    pass
