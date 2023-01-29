from app.db.db_connector import Database
from app.const.queries import *
from app.logic import markups
from app.const import states, classes
from app.logic import utils
import logging
from app.const.consts import *
from app.logic import memory
from random import randint, random, choice
from app.logic.utils import get_moscow_datetime
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import ReplyKeyboardRemove


class Controller:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.load_user_ids()

    def load_user_ids(self):
        memory.user_ids = self.db.get_all_user_ids()

    async def command_start(self, tg_id, name):
        self.db.add_empty_keyboard_hash(tg_id=tg_id)
        is_user_exist = self.db.is_user_exist_by_tg_id(tg_id=tg_id)
        if is_user_exist:
            text = '👋'
            markup = ReplyKeyboardRemove()
            await self.bot.send_message(
                chat_id=tg_id,
                text=text,
                reply_markup=markup,
                parse_mode='HTML'
            )
            text = choice(START_PHRASES)
        else:
            text = START_FOR_NEWBIES.format(name=name)
        is_admin = self.db.is_user_admin(tg_id=tg_id)
        markup = markups.start_menu_markup(is_admin=is_admin)
        return dict(text=text, markup=markup)

    async def get_instruction(self):
        text = INSTRUCTION
        markup = markups.back_to_start_markup()
        return dict(text=text, markup=markup)

    async def create_invitation(self, tg_id):
        user_id = self.db.get_user_id_by_tg_id(tg_id=tg_id)
        if not user_id:
            text = 'Для начала тебе нужно создать свой список подарков.\nДля этого просто нажми кнопку ⬇️'
            markup = markups.create_my_wishlist_markup()
        else:
            text = "<i>Разошли следующее сообщение своим друзьям:</i>"
            await self.bot.send_message(
                chat_id=tg_id,
                text=text,
                reply_markup=None,
                parse_mode='HTML'
            ) 
            text = FRIENDS_INVITATION_BY_CODE.format(code=user_id)
            markup = markups.back_to_start_markup()
        return dict(text=text, markup=markup)

    async def prepare_mailing_to_users(self, state):
        text = 'Введите сообщение, которое будет отправлено ВСЕМ пользователям, зарегистрированным в боте ' \
               '(но не заблокировавшим его).\nВ сообщении можно использовать смайлы и <b>средства HTML</b>.'
        markup = markups.back_to_start_markup()
        await state.set_state(states.Admin.mailing_text)
        return dict(text=text, markup=markup)

    async def confirm_mailing_to_users(self, message, state):
        async with state.proxy() as data:
            data['message_to_users'] = message.text
        text = f'Пример сообщения ниже. Отправляем?\n\n{message.text}'
        markup = markups.mailing_confirmation()
        return dict(text=text, markup=markup)

    async def send_mailing_to_users(self, state):
        try:
            async with state.proxy() as data:
                message_to_users = data['message_to_users']
        except KeyError:
            pass
        await state.finish()

        tg_id_list = self.db.get_all_users_tg_id()
        for tg_id in tg_id_list:
            try:
                await self.bot.send_message(
                    chat_id=tg_id, 
                    text=message_to_users, 
                    parse_mode='HTML'
                )
            except BotBlocked:
                pass
        text = 'Сообщение отправлено успешно!'
        markup = markups.start_menu_markup(is_admin=1)
        return dict(text=text, markup=markup)

    async def check_is_user_actual(self, from_user):
        print(f'from_user = {from_user}')
        user_data = dict(
            tg_id=from_user.id,
            name=from_user.first_name,
            last_name=from_user.last_name,
            tg_nickname=from_user.username
        )
        print(f'! user_data = {user_data}')
        is_user_actual = self.db.is_user_actual(user_data=user_data)
        print(f'is_user_actual = {is_user_actual}')
        return is_user_actual
        

    async def upsert_user_to_db(self, from_user):
        user_data = dict(
            name=from_user.first_name,
            last_name=from_user.last_name,
            tg_id=from_user.id,
            tg_nickname=from_user.username,
            registration_datetime=get_moscow_datetime()
        )
        user_id = self.db.get_user_id_by_tg_id(tg_id=from_user.id)
        print(f'user_id = {user_id}')
        if user_id:
            user_data['id'] = user_id
            print(f'user_data = {user_data}')
            self.db.update_user(user_data=user_data)
        else:
            while True:
                user_id = randint(100000, 999999)
                if user_id in memory.user_ids:
                    continue
                else:
                    memory.user_ids.append(user_id)
                    break
            user_data['id'] = user_id
            print(f'user_data = {user_data}')
            self.db.add_user(user_data=user_data)

    async def display_my_wishlist(self, tg_id):
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=tg_id, hashed=hashed)
        user_id = self.db.get_user_id_by_tg_id(tg_id=tg_id)
        wishes = self.db.get_wishes_by_tg_id(tg_id=tg_id)
        if wishes:
            for wish in wishes:
                wish_id = wish.pop('id')
                if wish['is_reserved']:
                    wish['is_reserved'] = '✅ - кто-то из твоих друзей решил исполнить это желание!'
                else:
                    wish['is_reserved'] = ''
                delete_wish_markup = markups.delete_wish_button(
                    wish_id=wish_id,
                    hashed=hashed,
                    is_wish_reserved=bool(wish['is_reserved'])
                )
                text = MY_WISH.format(
                    wish_name=wish['name'],
                    product_link=wish['product_link'] + '\n' if wish['product_link'] else '',
                    is_reserved=wish['is_reserved']
                )
                await self.bot.send_message(
                    chat_id=tg_id,
                    text=text,
                    reply_markup=delete_wish_markup,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )  
            text = MY_WISHES_BOTTOM.format(user_id=user_id)
        else:
            text = MY_WISHES_EMPTY_BOTTOM
        markup = markups.my_wishlist_markup()
        return dict(text=text, markup=markup)

    async def enter_wish_name(self, state):
        text = '<b>Опиши своё желание подробнее, чтобы друзья точно понимали, что ты хочешь.</b>\n\n' \
               'Например, <i>Книга "Гарри Поттер и философский камень"</i>'
        markup = markups.back_to_my_wishlist_markup()
        await state.set_state(states.Wish.wish_name_to_add)
        return dict(text=text, markup=markup)

    async def enter_list_wish_name(self, state):
        text = 'Введи несколько желаний, каждое с новой строки. ' \
               'Например:\n\n<i>Вертолетик на радиоуправлении\nСкейтборд\nКонструктор LEGO</i>'
        markup = markups.back_to_my_wishlist_markup()
        await state.set_state(states.Wish.wish_names_to_add)
        return dict(text=text, markup=markup)

    async def add_wish(self, tg_id, text, is_list_of_wishes):
        user_id = self.db.get_user_id_by_tg_id(tg_id=tg_id)

        wishes_user_already_has = self.db.count_user_wishes(user_id=user_id)
        if wishes_user_already_has > 30:
            text = 'Ты добавил уже больше 30 желаний. Больше мне в памяти не удержать.' \
                   'Попробуй удалить лишние.'
            await self.bot.send_message(
                    chat_id=tg_id,
                    text=text,
                    reply_markup=None,
                    parse_mode='HTML'
                )
        else:
            if is_list_of_wishes:
                wishes = text.split('\n')
            else:
                wishes = [text]
            for wish in wishes:
                wishlist_data = dict(
                    user_id=user_id,
                    name=wish
                )
                self.db.add_wish(wishlist_data=wishlist_data)

    async def get_keyboard_hash(self, tg_id):
        hashed = self.db.get_keyboard_hash(tg_id=tg_id)
        return hashed


    async def check_is_wish_reserved(self, wish_id):
        is_wish_reserved = self.db.is_wish_reserved(wish_id=wish_id)
        return is_wish_reserved

    async def get_wish_name(self, wish_id):
        wish_name = self.db.get_wish_name_by_id(wish_id=wish_id)
        return wish_name

    async def delete_wish_if_reserved(self, tg_id, wish_id, message_to_delete, keyboard_hash):
        text = '<b>Этот подарок забронирован одним из твоих друзей.</b> \nУдаляй его только если твой праздник уже прошел.'
        markup = markups.deleting_approval_button(
            wish_id=wish_id,
            hashed=keyboard_hash,
            message_to_delete=message_to_delete
        )
        return dict(text=text, markup=markup)

    async def delete_wish(self, wish_id):
        self.db.delete_wish(wish_id=wish_id)

    async def input_wish_link(self, state, wish_id):
        text = 'Отправь мне описание, которое хочешь добавить. Это может быть ссылка на товар, ссылка на изображение в интернете или что угодно.\n' \
               'К сожалению, картинки с твоего телефона я пока обрабатывать не умею.'
        markup = markups.back_to_my_wishlist_markup()
        async with state.proxy() as data:
            data['wish_id'] = wish_id
        await state.set_state(states.Wish.wish_link_to_add)
        return dict(text=text, markup=markup)

    async def add_wish_link(self, text, state):
        async with state.proxy() as data:
            self.db.add_wish_link(wish_id=data['wish_id'], link=text)
        await state.finish()

    async def display_wishes_reserved_by_me(self, tg_id):
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=tg_id, hashed=hashed)
        wishes = self.db.get_wishes_reserved_by_me(tg_id=tg_id)
        if wishes:
            for wish in wishes:
                wish_id = wish.pop('id')
                text = RESERVED_WISH.format(
                    wish_name=wish['wish_name'],
                    product_link=wish['product_link'] + '\n' if wish['product_link'] else '',
                    name=wish['username'] if wish['username'] else '',
                    last_name=wish['last_name'] if wish['last_name'] else '',
                    tg_nickname=wish['tg_nickname'] if wish['tg_nickname'] else ''
                )
                unreserve_wish_markup = markups.unreserve_wish_button(
                    wish_id=wish_id,
                    hashed=hashed
                )
                await self.bot.send_message(
                    chat_id=tg_id,
                    text=text,
                    reply_markup=unreserve_wish_markup,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            text = RESERVED_WISHES_BOTTOM
        else:
            text = RESERVED_WISHES_EMPTY_BOTTOM
        markup = markups.wishes_reseved_by_me_markup()
        return dict(text=text, markup=markup)

    async def unreserve_wish(self, wish_id, tg_id):
        self.db.unreserve_wish(wish_id=wish_id, tg_id_who_chose=tg_id)

    async def enter_friends_code(self, tg_id, state):
        text = 'Введи <b>шестизначный код</b> друга.\n' \
               'Или выбери из недавно просмотренных друзей.'
        last_viewed_data = self.db.get_user_last_viewed_id(tg_id=tg_id)
        markup = markups.last_viewed_friends_markup(last_viewed_data=last_viewed_data)
        await state.set_state(states.Friend.friend_code)
        return dict(text=text, markup=markup)

    async def get_friend_user_id(self, query):
        tg_id = query.from_user.id
        friend_user_id = utils.code_processing(input=query.text)

        is_user_exist = self.db.is_user_exist_by_user_id(user_id=friend_user_id)
        if not is_user_exist:
            raise classes.UserNotFound

        user_id = self.db.get_user_id_by_tg_id(tg_id=tg_id)
        if user_id == friend_user_id:
            raise classes.UserIsYou
            
        return friend_user_id

    async def add_last_viewed_id(self, my_tg_id, friend_user_id):
        user_id = self.db.get_user_id_by_tg_id(tg_id=my_tg_id)
        self.db.add_last_viewed_id(
            user_id=user_id,
            friend_user_id=friend_user_id
        )

    async def display_friends_wishlist(self, my_tg_id, friend_user_id):
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=my_tg_id, hashed=hashed)
        number_of_wishes_reserved_by_me = self.db.how_many_wishes_are_reserved(
            friend_user_id=friend_user_id,
            my_tg_id=my_tg_id
        )
        user_info = self.db.get_user_info_by_user_id(user_id=friend_user_id)
        wishes = self.db.get_available_wishes_by_user_id(user_id=friend_user_id)
        if wishes:
            for wish in wishes:
                wish_id = wish.pop('id')
                text = FRIEND_WISH.format(
                    wish_name=wish["name"],
                    product_link=wish["product_link"] if wish["product_link"] else ''
                )
                if number_of_wishes_reserved_by_me < 2:
                    reserve_wish_markup = markups.reserve_wish_button(
                        wish_id=wish_id,
                        hashed=hashed
                    )
                else:
                    reserve_wish_markup = None
                await self.bot.send_message(
                    chat_id=my_tg_id,
                    text=text,
                    reply_markup=reserve_wish_markup,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            if number_of_wishes_reserved_by_me < 2:
                text = FRIEND_WISHES_BOTTOM.format(
                    name=user_info['name'] if user_info['name'] else '', 
                    last_name=user_info['last_name'] if user_info['last_name'] else '',
                    tg_nickname=user_info['tg_nickname'] if user_info['tg_nickname'] else ''
                )
            else:
                text = FRIENDS_WISHES_BLOCKED.format(
                    name=user_info['name'] if user_info['name'] else '', 
                    last_name=user_info['last_name'] if user_info['last_name'] else '',
                    tg_nickname=user_info['tg_nickname'] if user_info['tg_nickname'] else ''
                )
        else:
            text = FRIEND_WISHES_EMPTY_BOTTOM.format(
                    name=user_info['name'] if user_info['name'] else '', 
                    last_name=user_info['last_name'] if user_info['last_name'] else '',
                    tg_nickname=user_info['tg_nickname'] if user_info['tg_nickname'] else ''
            )
        markup = markups.friend_wishlist_markup()
        return dict(text=text, markup=markup)

    async def reserve_wish(self, wish_id, tg_id):
        self.db.reserve_wish(wish_id=wish_id, tg_id_who_chose=tg_id)
