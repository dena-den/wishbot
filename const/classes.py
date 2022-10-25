from aiogram.utils.callback_data import CallbackData


WishToDelete = CallbackData('delete', 'wish_id')
WishToReserve = CallbackData('reserve', 'wish_id')
WishToUnreserve = CallbackData('unreserve', 'wish_id')
AddLink = CallbackData('add_link', 'wish_id')
