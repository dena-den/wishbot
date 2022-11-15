import logging
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import *
from app.logic.decorators import *
from app.logic.middlewares import LoggingMiddleware, ThrottlingMiddleware
from app.logic.controller import Controller
from app.const import classes, states
from app.logic import markups

#! temp
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
@dp.message_handler(Text(equals='Назад в стартовое меню'), state='*')
@rate_limit(1)
async def command_start_process(message: types.Message, state: FSMContext):
    response = await c.command_start(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(commands='instruction', state='*')
@dp.message_handler(Text(equals='Как со мной общаться?'), state='*')
@rate_limit(1)
async def get_instruction_process(message: types.Message):
    response = await c.get_instruction()
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(commands='invitation', state='*')
@dp.message_handler(Text(equals='Разослать мой список друзьям'), state='*')
@rate_limit(1)
async def create_invitation_process(message: types.Message):
    tg_id = message.from_user.id
    response = await c.create_invitation(tg_id=tg_id)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(equals='Создать мой список желаний'), state='*')
@dp.message_handler(Text(equals='Назад к вводу имени'), state='*')
@rate_limit(1)
async def enter_name_process(message: types.Message, state: FSMContext):
    is_user_exist = await c.check_is_user_exist(tg_id=message.from_user.id)
    if not is_user_exist:
        response = await c.enter_name(message=message, state=state)
    else:
        tg_id = message.from_user.id
        response = await c.display_my_wishlist(tg_id=tg_id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.User.name)
@dp.message_handler(Text(equals='Назад к вводу даты рождения'), state='*')
@rate_limit(1)
async def enter_birthdate_process(message: types.Message, state: FSMContext):
    response = await c.enter_birthdate(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.User.birthdate)
@dp.message_handler(Text(equals='Назад к вводу телефона'), state='*')
@rate_limit(1)
async def enter_phone_process(message: types.Message, state: FSMContext):
    response = await c.enter_phone(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(content_types=['contact'], 
                    state=states.User.phone)
@rate_limit(1)
async def check_data_with_phone_process(message: types.Message, state: FSMContext):
    response = await c.check_data(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )
        

@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/', 'Все')),
                    state=states.User.phone)
@rate_limit(1)
async def check_data_no_phone_process(message: types.Message, state: FSMContext):
    if message.text == 'Не хочу сообщать':
        response = await c.check_data(message=message, state=state)
    else:
        response = dict(
            text='Пожалуйста, воспользуйтесь кнопкой "Поделиться номером телефона".',
            markup=markups.back_to_markup(to='birthdate')
        )
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )



@dp.message_handler(commands='my_wishes', state='*')
@dp.message_handler(Text(equals='Открыть мой список желаний'), state='*')
@dp.message_handler(Text(equals='Все правильно'), state=states.User.phone)
@dp.message_handler(Text(equals='Назад к списку'), state='*')
@rate_limit(1)
async def display_my_wishlist_process(message: types.Message, state: FSMContext):
    if message.text == 'Все правильно':
        await c.add_user_to_db(message=message, state=state)
    is_user_exist = await c.check_is_user_exist(tg_id=message.from_user.id)
    if is_user_exist:
        tg_id = message.from_user.id
        response = await c.display_my_wishlist(tg_id=tg_id, state=state)
    else:
        response = await c.command_start(message=message, state=state)
        response['text'] = 'Для начала нужно создать список подарков'
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(equals='Добавить желание'))
@rate_limit(1)
async def enter_wish_name_process(message: types.Message, state: FSMContext):
    response = await c.enter_wish_name(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.Wish.wish_name_to_add)
@rate_limit(1)
async def add_wish_process(message: types.Message, state: FSMContext):
    await c.add_wish(message=message, state=state, is_list_of_wishes=0)
    response = await c.display_my_wishlist(tg_id=message.from_user.id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(equals='Добавить желания списком'))
@rate_limit(1)
async def enter_list_wish_name_process(message: types.Message, state: FSMContext):
    response = await c.enter_list_wish_name(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.Wish.wish_names_to_add)
@rate_limit(1)
async def add_wish_list_process(message: types.Message, state: FSMContext):
    await c.add_wish(message=message, state=state, is_list_of_wishes=1)
    response = await c.display_my_wishlist(tg_id=message.from_user.id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.callback_query_handler(classes.WishToDelete.filter(), state='*')
@rate_limit(1)
async def delete_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        return
    await query.answer('Подарок удален')
    await c.delete_wish(wish_id=callback_data['wish_id'])
    response = await c.display_my_wishlist(tg_id=tg_id, state=state)
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'],
                        parse_mode='HTML')


@dp.callback_query_handler(classes.AddLink.filter(), state='*')
@rate_limit(1)
async def input_wish_link_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        return
    await query.answer()
    response = await c.input_wish_link(state=state, wish_id=callback_data['wish_id'])
    await bot.send_message(chat_id=query.from_user.id,
                           text=response['text'],
                           reply_markup=response['markup'],
                           parse_mode='HTML')


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.Wish.wish_link_to_add)
@rate_limit(1)
async def add_wish_link_process(message: types.Message, state: FSMContext):
    await c.add_wish_link(state=state, wish_link=message.text)
    response = await c.display_my_wishlist(tg_id=message.from_user.id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(commands='reserved_wishes', state='*')
@dp.message_handler(Text(equals='Забронированные мною подарки'), state='*')
@rate_limit(1, 'key')
async def display_wishes_reserved_by_me_process(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(commands='friend_wishes', state='*')
@dp.message_handler(Text(equals='Выбрать подарок другу'))
@dp.message_handler(Text(equals='Назад к введению кода'), state='*')
@rate_limit(1)
async def enter_friends_code_process(message: types.Message, state: FSMContext):
    response = await c.enter_friends_code(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.Friend.friend_code)
@rate_limit(1)
async def display_friends_wishlist_process(message: types.Message, state: FSMContext):
    try:
        friend_user_id = await c.get_friend_user_id(message=message, state=state)
        response = await c.display_friends_wishlist(my_tg_id=message.from_user.id, friend_user_id=friend_user_id)
    except classes.ProhibitedSymbols:
        response = dict(
            text='Код состоит только из цифр. Буквы отсутствуют! Попробуй еще раз.',
            markup=markups.back_to_markup(to='start')
        )
    except classes.UserNotFound:
        response = dict(
            text='Пользователя с таким кодом не найдено. Ничего не перепутал? Попробуй еще раз.\n' \
                 'Если вводишь номер телефона, то начинай с 7ки.',
            markup=markups.back_to_markup(to='start')
        )
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.callback_query_handler(classes.WishToReserve.filter(), state='*')
@rate_limit(1)
async def reserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        return
    await query.answer('Подарок выбран')
    await c.reserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id, state=state)
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'],
                        parse_mode='HTML')


@dp.callback_query_handler(classes.WishToUnreserve.filter(), state='*')
@rate_limit(1)
async def unreserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    db_hash = await c.get_keyboard_hash(tg_id=tg_id)
    received_hash = int(callback_data['hashed'])
    if db_hash != received_hash:
        return
    await query.answer('Подарок отменен')
    await c.unreserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id, state=state)
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'],
                        parse_mode='HTML')


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


@dp.errors_handler(exception=Exception)
async def botblocked_error_handler(update: types.Update, e):
    logging.warning("Error occured")
    logging.warning(e)
    return True"""
