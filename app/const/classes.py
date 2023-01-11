from aiogram.utils.callback_data import CallbackData


Start = CallbackData('start')
# CreateWishlist = CallbackData('create_wishlist')
MyWishlist = CallbackData('my_wishlist')
ChooseWish = CallbackData('choose_wish')
ReservedWishes = CallbackData('reserved_wishes')
Invitation = CallbackData('invitation')
Instruction = CallbackData('instruction')

# EnterName = CallbackData('enter_name')
# EnterBirthdate = CallbackData('enter_birthdate')
# EnterPhone = CallbackData('enter_phone')
# UseSixDigitCode = CallbackData('use_six_digit_code')

AddWish = CallbackData('add_wish')
AddWishes = CallbackData('add_wishes')
WishToDelete = CallbackData('delete', 'wish_id', 'hashed', 'is_reserved')
WishToReserve = CallbackData('reserve', 'wish_id', 'hashed')
WishToUnreserve = CallbackData('unreserve', 'wish_id', 'hashed')
AddLink = CallbackData('add_link', 'wish_id', 'hashed')
LastViewedId = CallbackData('last_viewed', 'friend_user_id')

EmptyCallback = CallbackData('empty')


class CodeNotValid(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class UserIsYou(BaseException):
    pass
