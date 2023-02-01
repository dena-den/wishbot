import logging
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.utils.exceptions import *
from app.logic.decorators import *
from app.logic.middlewares import LoggingMiddleware, ThrottlingMiddleware
from app.logic.controller import Controller
from app.const import classes, states
from app.logic import markups
from typing import Optional, Union
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv("BOT_TOKEN"))
Bot.set_current(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(ThrottlingMiddleware(dispatcher=dp))
c = Controller(bot=bot)


@dp.message_handler(commands='start', state='*')
@dp.callback_query_handler(classes.Start.filter(), state='*')
@rate_limit(1, 'start')
async def command_start_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    is_user_actual = await c.check_is_user_actual(from_user=query.from_user)
    if not is_user_actual:
        await c.upsert_user_to_db(from_user=query.from_user)
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    name = query.from_user.first_name
    response = await c.command_start(tg_id=tg_id, name=name)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(commands='instruction', state='*')
@dp.callback_query_handler(classes.Instruction.filter(), state='*')
@rate_limit(1, 'instruction')
async def get_instruction_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    response = await c.get_instruction()
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(commands='invitation', state='*')
@dp.callback_query_handler(classes.Invitation.filter(), state='*')
@rate_limit(1, 'invitation')
async def create_invitation_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    response = await c.create_invitation(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.MailingMessage.filter(), state='*')
@rate_limit(1, 'prepare_mailing')
async def prepare_mailing_to_users_process(
    query: types.CallbackQuery,
    state: FSMContext
):
    tg_id = query.from_user.id
    await query.answer()
    response = await c.prepare_mailing_to_users(state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(state=states.Admin.mailing_text)
@rate_limit(1, 'confirm_mailing')
async def confirm_mailing_to_users_process(
    message: types.Message,
    state: FSMContext
):
    tg_id = message.from_user.id
    response = await c.confirm_mailing_to_users(message=message, state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.MailingSend.filter(), state='*')
@rate_limit(1, 'send_mailing')
async def send_mailing_to_users_process(
    query: types.CallbackQuery,
    state: FSMContext
):
    tg_id = query.from_user.id
    await query.answer()
    await query.message.delete()
    response = await c.send_mailing_to_users(state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(commands='my_wishes', state='*')
@dp.callback_query_handler(classes.MyWishlist.filter(), state='*')
@rate_limit(1, 'my_wishlist')
async def display_my_wishlist_callback_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    response = await c.display_my_wishlist(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.AddWish.filter(), state='*')
@rate_limit(1, 'add_wish')
async def enter_wish_name_process(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.from_user.id
    await query.answer()
    response = await c.enter_wish_name(state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(state=states.Wish.wish_name_to_add)
@rate_limit(1, 'add_wish_process')
async def add_wish_process(message: types.Message, state: FSMContext):
    await state.finish()
    tg_id = message.from_user.id
    text = message.text
    await c.add_wish(tg_id=tg_id, text=text, is_list_of_wishes=0)
    response = await c.display_my_wishlist(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.AddWishes.filter(), state='*')
@rate_limit(1, 'add_wishes')
async def enter_list_wish_name_process(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.from_user.id
    await query.answer()
    response = await c.enter_list_wish_name(state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(state=states.Wish.wish_names_to_add)
@rate_limit(1, 'add_wishes_process')
async def add_wish_list_process(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    text = message.text
    await c.add_wish(tg_id=tg_id, text=text, is_list_of_wishes=1)
    response = await c.display_my_wishlist(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.WishToDelete.filter(), state='*')
@rate_limit(1, 'delete_wish')
async def delete_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        await query.answer()
        return
    if callback_data['is_reserved'] == 'True':
        message_to_delete = f'{query.message.chat.id}/{query.message.message_id}'
        response = await c.delete_wish_if_reserved(
            tg_id=tg_id,
            wish_id=callback_data['wish_id'],
            message_to_delete=message_to_delete,
            keyboard_hash = received_hash
        )    
        await query.answer()
        await bot.send_message(
            chat_id=tg_id,
            text=response['text'],
            reply_markup=response['markup'],
            parse_mode='HTML'
        )
    else:
        await c.delete_wish(wish_id=callback_data['wish_id'])
        await query.message.delete()
        if callback_data['message_to_delete']:
            chat_id, message_id = callback_data['message_to_delete'].split('/')
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        await query.answer('Подарок удален')


@dp.callback_query_handler(classes.AddLink.filter(), state='*')
@rate_limit(1, 'input_wishlink')
async def input_wish_link_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        await query.answer()
        return
    await query.answer()
    response = await c.input_wish_link(state=state, wish_id=callback_data['wish_id'])
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(state=states.Wish.wish_link_to_add)
@rate_limit(1, 'add_wish_link')
async def add_wish_link_process(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    text = message.text
    await c.add_wish_link(text=text, state=state)
    response = await c.display_my_wishlist(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(commands='reserved_wishes', state='*')
@dp.callback_query_handler(classes.ReservedWishes.filter(), state='*')
@rate_limit(1, 'reserved_wishes')
async def display_wishes_reserved_by_me_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(commands='find_friend', state='*')
@dp.callback_query_handler(classes.FindFriend.filter(), state='*')
@rate_limit(1, 'find_friend_wishlist')
async def enter_friends_code_process(
    query: Union[types.CallbackQuery, types.Message],
    state: FSMContext
):
    await state.finish()
    tg_id = query.from_user.id
    if isinstance(query, types.CallbackQuery):
        await query.answer()
    await state.finish()
    response = await c.enter_friends_code(tg_id=tg_id, state=state)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.message_handler(state=states.Friend.friend_code)
@rate_limit(1, 'friend_wishlist')
async def display_friends_wishlist_process(query: types.CallbackQuery, state: FSMContext):
    try:
        tg_id = query.from_user.id
        is_user_actual = await c.check_is_user_actual(from_user=query.from_user)
        if not is_user_actual:
            await c.upsert_user_to_db(from_user=query.from_user)
        friend_user_id = await c.get_friend_user_id(query=query)
        await c.add_last_viewed_id(my_tg_id=tg_id, friend_user_id=friend_user_id)
        response = await c.display_friends_wishlist(my_tg_id=tg_id, friend_user_id=friend_user_id)
        await state.finish()
    except classes.CodeNotValid:
        response = dict(
            text='Код должен состоять только из 6 цифр. Попробуй еще раз.',
            markup=markups.back_to_start_markup()
        )
    except classes.UserNotFound:
        response = dict(
            text='Пользователя с таким кодом не найдено. Ничего не перепутал? Попробуй еще раз.',
            markup=markups.back_to_start_markup()
        )
    except classes.UserIsYou:
        response = await c.display_my_wishlist(tg_id=tg_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.LastViewedId.filter(), state='*')
@rate_limit(1, 'latest_friend_wishlist')
async def display_latest_friend_wishlist_process(
    query: types.CallbackQuery, callback_data: dict
    ):
    tg_id = query.from_user.id
    friend_user_id = callback_data['friend_user_id']
    await query.answer()
    await c.add_last_viewed_id(my_tg_id=tg_id, friend_user_id=friend_user_id)
    response = await c.display_friends_wishlist(my_tg_id=tg_id, friend_user_id=friend_user_id)
    await bot.send_message(
        chat_id=tg_id,
        text=response['text'],
        reply_markup=response['markup'],
        parse_mode='HTML'
    )


@dp.callback_query_handler(classes.WishToReserve.filter(), state='*')
@rate_limit(1, 'reserve_wish')
async def reserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        await query.answer()
        return
    is_wish_reserved = await c.check_is_wish_reserved(wish_id=callback_data['wish_id'])
    if not is_wish_reserved:
        await c.reserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
        await query.answer('Подарок выбран')
        await query.message.delete()
    else:
        await query.answer('Простите, кто-то уже выбрал этот подарок, попробуйте другой.')


@dp.callback_query_handler(classes.WishToUnreserve.filter(), state='*')
@rate_limit(1, 'unreserve_wish')
async def unreserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        await query.answer()
        return
    await c.unreserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
    await query.answer('Подарок отменен')
    await query.message.delete()


@dp.callback_query_handler(classes.EmptyCallback.filter(), state='*')
@rate_limit(1, 'empty_callback')
async def empty_callback_process(query: types.CallbackQuery, state: FSMContext):
    await query.answer()


@dp.callback_query_handler(classes.Cancel.filter(), state='*')
@rate_limit(1, 'cancel_callback')
async def cancel_callback_process(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()


"""@dp.message_handler(Text(equals="Notification"))
async def message_main_menu_button_notification_process(message: types.Message):
    response = await c.message_main_menu_buttons_click(message=message)
    await message.reply(
        text=response["text"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(contains="button"))
async def message_main_menu_buttons_click_process(message: types.Message):
    response = await c.message_main_menu_buttons_click(message=message)
    await message.reply(
        text=response["text"],
        parse_mode="HTML",
        reply=False
    )


@dp.errors_handler(exception=RateLimitException)
async def too_many_requests_error_handler(update, error):
    logging.warning(f"{error} is catched.")

"""
