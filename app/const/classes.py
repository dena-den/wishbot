from aiogram.utils.callback_data import CallbackData


Start = CallbackData('start')
MyWishlist = CallbackData('my_wishlist')
FindFriend = CallbackData('choose_wish')
ReservedWishes = CallbackData('reserved_wishes')
Invitation = CallbackData('invitation')
Instruction = CallbackData('instruction')

AddWish = CallbackData('add_wish')
AddWishes = CallbackData('add_wishes')
WishToDelete = CallbackData('delete', 'wish_id', 'hashed', 'is_reserved', 'message_to_delete')
WishToReserve = CallbackData('reserve', 'wish_id', 'hashed')
WishToUnreserve = CallbackData('unreserve', 'wish_id', 'hashed')
AddLink = CallbackData('add_link', 'wish_id', 'hashed')
LastViewedId = CallbackData('last_viewed', 'friend_user_id')
MailingMessage = CallbackData('mailing_message')
MailingSend = CallbackData('mailing_send')

Cancel = CallbackData('cancel')
EmptyCallback = CallbackData('empty')


class CodeNotValid(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserIsYou(BaseException):
    pass
