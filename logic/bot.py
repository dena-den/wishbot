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


@dp.message_handler(Text(equals='Создать мой список подарков'))
@dp.message_handler(Text(equals='Назад к вводу имени'), state='*')
async def enter_name_process(message: types.Message, state: FSMContext):
    response = await c.enter_name(message=message, state=state)
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


@dp.message_handler(lambda msg: not msg.text.startswith(('Назад', 'Все', '/')),
                    state=states.User.phone)
async def check_data_process(message: types.Message, state: FSMContext):
    response = await c.check_data(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


@dp.message_handler(Text(equals='Открыть мой список подарков'), state='*')
@dp.message_handler(Text(equals='Все правильно'), state=states.User.phone)
@dp.message_handler(Text(equals='Назад к списку'), state=states.Wish.wish_name_to_add)
async def display_my_wishlist_process(message: types.Message, state: FSMContext):
    if message.text == 'Все правильно':
        await c.add_user_to_db(message=message, state=state)
    is_user_exist = await c.check_is_user_exist(tg_id=message.from_user.id)
    if is_user_exist:
        response = await c.display_my_wishlist(message=message, state=state)
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
    response = await c.display_my_wishlist(message=message, state=state)
    await message.reply(
        text=response["text"],
        reply_markup=response["markup"],
        parse_mode="HTML",
        reply=False
    )


# @dp.callback_query_handler()
# async def del_point_from_list_process(query: CallbackQuery):
#     response = await c.del_point_from_list(query=query)
#     await bot.send_message(chat_id=query.from_user.id,
#                         text=response['text'],
#                         reply_markup=response['markup'])


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
