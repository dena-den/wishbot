import logging
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import *
from .decorators import *
from .middlewares import LoggingMiddleware, ThrottlingMiddleware
from .controller import Controller
from const import classes
from const import states
from logic import markups

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
#@rate_limit(2, "start")
async def command_start_process(message: types.Message, state: FSMContext):
    response = await c.command_start(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(commands='instruction', state='*')
@dp.message_handler(Text(equals='Инструкция к пользованию'), state='*')
async def get_instruction_process(message: types.Message):
    response = await c.get_instruction()
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(equals='Создать мой список подарков'), state='*')
@dp.message_handler(Text(equals='Назад к вводу имени'), state='*')
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
@dp.message_handler(Text(equals='Открыть мой список подарков'), state='*')
@dp.message_handler(Text(equals='Все правильно'), state=states.User.phone)
@dp.message_handler(Text(equals='Назад к списку'), state=states.Wish.wish_name_to_add)
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


@dp.message_handler(Text(equals='Добавить подарок'))
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
async def add_wish_process(message: types.Message, state: FSMContext):
    await c.add_wish(message=message, state=state)
    response = await c.display_my_wishlist(tg_id=message.from_user.id, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.callback_query_handler(classes.WishToDelete.filter(), state='*')
async def delete_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await c.delete_wish(wish_id=callback_data['wish_id'])
    tg_id = query.from_user.id
    deleted_wish_name = await c.get_wish_name(wish_id=callback_data['wish_id'])
    response = await c.display_my_wishlist(tg_id=tg_id, state=state)
    response['text'] = f'Подарок "{deleted_wish_name}" удален.'
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'])


@dp.callback_query_handler(classes.AddLink.filter(), state='*')
async def input_wish_link_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    response = await c.input_wish_link(state=state, wish_id=callback_data['wish_id'])
    await bot.send_message(chat_id=query.from_user.id,
                           text=response['text'],
                           reply_markup=response['markup'])


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', '/')),
                    state=states.Wish.wish_link_to_add)
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
async def display_friends_wishlist_process(message: types.Message, state: FSMContext):
    friend_user_id = await c.get_friend_user_id(message=message, state=state)
    response = await c.display_friends_wishlist(my_tg_id=message.from_user.id, friend_user_id=friend_user_id)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.callback_query_handler(classes.WishToReserve.filter(), state='*')
async def reserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    await c.reserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id, state=state)
    response['text'] = '<b>Подарок успешно забронирован!</b>\n\n' + response['text']
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'],
                        parse_mode='HTML')


@dp.callback_query_handler(classes.WishToUnreserve.filter(), state='*')
async def unreserve_wish_process(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    tg_id = query.from_user.id
    await c.unreserve_wish(wish_id=callback_data['wish_id'], tg_id=tg_id)
    response = await c.display_wishes_reserved_by_me(tg_id=tg_id, state=state)
    await bot.send_message(chat_id=tg_id,
                        text=response['text'],
                        reply_markup=response['markup'])


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
