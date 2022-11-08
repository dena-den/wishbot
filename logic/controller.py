from db.db_connector import Database
from const.queries import *
from . import markups
from const import states, classes
import re
from logic import utils
import logging
from const.consts import *
from logic import memory
from random import randint, random


class Controller:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.load_user_ids()

    def load_user_ids(self):
        memory.user_ids = self.db.get_all_user_ids()

    async def command_start(self, message, state):
        await state.finish()
        self.db.add_empty_keyboard_hash(tg_id=message.from_user.id)
        name = message.from_user.first_name
        is_user_exist = self.db.is_user_exist_by_tg_id(tg_id=message.from_user.id)
        if is_user_exist:
            text = START.format(name=name)
        else:
            text = START_FOR_NEWBIES.format(name=name)
        markup = markups.start_menu_markup(is_user_exist=is_user_exist)
        return dict(text=text, markup=markup)

    async def get_instruction(self):
        text = INSTRUCTION
        markup = markups.back_to_markup(to='start')
        return dict(text=text, markup=markup)

    async def enter_name(self, message, state):
        text = "Для начала мне нужно с тобой совсем немного познакомиться." \
               "<b>1/3</b> Введи свое имя (можно с фамилией). Его будут видеть твои друзья."
        markup = markups.back_to_markup(to='start')
        await state.set_state(states.User.name)
        return dict(text=text, markup=markup)

    async def enter_birthdate(self, message, state):
        name_pattern = r'[ёЁА-Яа-я- A-za-z]+'
        user_data = message.text
        if not user_data.startswith('Назад'):
            if re.fullmatch(name_pattern, user_data) and len(user_data) < 128:
                async with state.proxy() as data:
                    data['name'] = user_data
                text = "<b>2/3</b> Введи дату рождения, чтобы друзья точно знали, когда у тебя праздник!"
                markup = markups.back_to_markup(to='name')
                await state.set_state(states.User.birthdate)
            elif not len(user_data) < 64:
                text = "<b>1/3</b> Слишком длинное имя. Можно обращаться к тебе как-то покороче? Введи имя еще раз."
                markup = markups.back_to_markup(to='start')
            else:
                text = "<b>1/3</b> Интересное у тебя имя, но нам такое не подойдет. " \
                       "Я понимаю только буквы и тире. Введи еще раз."
                markup = markups.back_to_markup(to='start')
        else:
            text = "<b>2/3</b> Введи дату рождения, чтобы друзья точно знали, когда у тебя праздник!"
            markup = markups.back_to_markup(to='name')
            await state.set_state(states.User.birthdate)
        return dict(text=text, markup=markup)

    async def enter_phone(self, message, state):
        user_data = message.text
        birthdate = utils.birthdate_processing(input=user_data)
        if not user_data.startswith('Назад'):
            if birthdate:
                async with state.proxy() as data:
                    data['birthdate'] = birthdate
                text = "<b>3/3</b> Поделись своим номером телефона, чтобы твоим друзьям было проще тебя найти. " \
                       "Но это совсем необязательно."
                markup = markups.back_to_markup(to='birthdate')
                await state.set_state(states.User.phone)
            else:
                text = '<b>2/3</b> Что это за день такой? Введи, пожалуйста, дату в формате ДД.ММ.ГГГГ \n' \
                       'Например, <i>20.11.2022</i>'
                markup = markups.back_to_markup(to='name')
        else:
            text = "<b>3/3</b> Поделись своим номером телефона, чтобы твоим друзьям было проще тебя найти. " \
                   "Но это совсем необязательно."
            markup = markups.back_to_markup(to='birthdate')
            await state.set_state(states.User.phone)
        return dict(text=text, markup=markup)

    async def check_data(self, message, state):
        async with state.proxy() as data:
            if message.text == 'Не хочу сообщать':
                data['phone'] = None
            else:
                data['phone'] = message.contact.phone_number.strip('+')
            user_data = ', '.join([str(value) for value in data.values() if value])
            text = "Я все правильно записал? Проверь, пожалуйста:\n" \
                   f"{user_data}"
        markup = markups.back_to_markup(to='phone')
        return dict(text=text, markup=markup)

    async def add_user_to_db(self, message, state):
        while True:
            user_id = randint(100000, 999999)
            if user_id in memory.user_ids:
                continue
            else:
                memory.user_ids.append(user_id)
                break
        async with state.proxy() as data:
            user_data = dict(
                id=user_id,
                name=data['name'],
                birthdate=data['birthdate'],
                phone=data['phone'],
                tg_id=message.from_user.id,
                tg_nickname=message.from_user.username
            )
            self.db.add_user(user_data=user_data)
        await state.finish()

    async def display_my_wishlist(self, tg_id, state):
        await state.finish()
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=tg_id, hashed=hashed)
        user_id = self.db.get_user_id_by_tg_id(tg_id=tg_id) 
        wishes = self.db.get_wishes_by_tg_id(tg_id=tg_id)
        if wishes:
            text = WISHES_TOP
            await self.bot.send_message(chat_id=tg_id,
                    text=text,
                    reply_markup=None,
                    parse_mode='HTML')
            for wish in wishes:
                wish_id = wish.pop('id')
                delete_button_disabled = bool(wish['is_reserved'])
                add_link_button_disabled = bool(wish['product_link'])
                wish['is_reserved'] = '🔒' if wish['is_reserved'] else '🆓'
                delete_wish_markup = markups.delete_wish_button(
                    wish_id=wish_id,
                    hashed=hashed,
                    delete_button_disabled=delete_button_disabled,
                    add_link_button_disabled=add_link_button_disabled
                )
                text = "\n".join([str(row) for row in wish.values() if row])
                await self.bot.send_message(chat_id=tg_id,
                                    text=text,
                                    reply_markup=delete_wish_markup,
                                    parse_mode='HTML')       
            text = MY_WISHES_BOTTOM.format(user_id=user_id)
        else:
            text = MY_WISHES_EMPTY_BOTTOM.format(user_id=user_id)
        markup = markups.my_wishlist_markup()
        return dict(text=text, markup=markup)

    async def enter_wish_name(self, message, state):
        text = '<b>Опиши своё желание подробнее, чтобы друзья точно понимали, что ты хочешь.</b>\n\n' \
               'Например, <i>Книга "Гарри Поттер и философский камень"</i>'
        markup = markups.back_to_markup(to='wishlist')
        await state.set_state(states.Wish.wish_name_to_add)
        return dict(text=text, markup=markup)

    async def enter_list_wish_name(self, message, state):
        text = 'Введи несколько желаний, каждое с новой строки. ' \
               'Например:\n\n<i>Вертолетик на радиоуправлении\nСкейтборд\nКонструктор LEGO</i>'
        markup = markups.back_to_markup(to='wishlist')
        await state.set_state(states.Wish.wish_names_to_add)
        return dict(text=text, markup=markup)

    async def get_keyboard_hash(self, tg_id):
        hashed = self.db.get_keyboard_hash(tg_id=tg_id)
        return hashed

    async def check_is_user_exist(self, tg_id):
        is_user_exist = self.db.is_user_exist_by_tg_id(tg_id=tg_id)
        return is_user_exist

    async def get_wish_name(self, wish_id):
        wish_name = self.db.get_wish_name_by_id(wish_id=wish_id)
        return wish_name

    async def add_wish(self, message, state, is_list_of_wishes):
        user_id = self.db.get_user_id_by_tg_id(tg_id=message.from_user.id)
        if is_list_of_wishes:
            wishes = message.text.split('\n')
        else:
            wishes = [message.text]
        for wish in wishes:
            wishlist_data = dict(
                user_id=user_id,
                name=wish
            )
            self.db.add_wish(wishlist_data=wishlist_data)

    async def delete_wish(self, wish_id):
        self.db.delete_wish(wish_id=wish_id)

    async def input_wish_link(self, state, wish_id):
        text = 'Отправьте мне ссылку, которую хотите добавить'
        markup = markups.back_to_markup(to='start')
        await state.set_state(states.Wish.wish_link_to_add)
        async with state.proxy() as data:
            data['wish_id'] = wish_id
        return dict(text=text, markup=markup)

    async def add_wish_link(self, state, wish_link):
        async with state.proxy() as data:
            self.db.add_wish_link(wish_id=data['wish_id'], link=wish_link)
        await state.finish()

    async def display_wishes_reserved_by_me(self, tg_id, state):
        await state.finish()
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=tg_id, hashed=hashed)
        wishes = self.db.get_wishes_reserved_by_me(tg_id=tg_id)
        if wishes:
            text = WISHES_TOP
            await self.bot.send_message(chat_id=tg_id,
                    text=text,
                    reply_markup=None,
                    parse_mode='HTML')
            for wish in wishes:
                wish_id = wish.pop('id')
                text = RESERVED_WISH.format(
                    wish_name=wish['wish_name'],
                    product_link=wish['product_link'] + '\n' if wish['product_link'] else '',
                    name=wish['username'],
                    birthdate=wish['birthdate']
                )
                unreserve_wish_markup = markups.unreserve_wish_button(
                    wish_id=wish_id,
                    hashed=hashed
                )
                await self.bot.send_message(chat_id=tg_id,
                                            text=text,
                                            reply_markup=unreserve_wish_markup,
                                            parse_mode='HTML')
            text = RESERVED_WISHES_BOTTOM
        else:
            text = RESERVED_WISHES_EMPTY_BOTTOM
        markup = markups.wishes_reseved_by_me_markup()
        return dict(text=text, markup=markup)

    async def unreserve_wish(self, wish_id, tg_id):
        self.db.unreserve_wish(wish_id=wish_id, tg_id_who_chose=tg_id)

    async def enter_friends_code(self, message, state):
        text = 'Введите номер телефона друга или его 6-ти значный код.'
        markup = markups.back_to_markup(to='start')
        await state.set_state(states.Friend.friend_code)
        return dict(text=text, markup=markup)

    async def get_friend_user_id(self, message, state):
        received_code = utils.code_processing(input=message.text)
        if len(received_code) == 6:
            friend_user_id = int(received_code)
        else:
            friend_user_id = self.db.get_user_id_by_phone(phone=int(received_code))
        is_user_exist = self.db.is_user_exist_by_user_id(user_id=friend_user_id)
        if not is_user_exist:
            raise classes.UserNotFound
        else:
            await state.finish()
        return friend_user_id

    async def display_friends_wishlist(self, my_tg_id, friend_user_id):
        hashed = hash(random())
        self.db.update_keyboard_hash(tg_id=my_tg_id, hashed=hashed)
        number_of_wishes_reserved_by_me = self.db.how_many_wishes_are_reserved(
            friend_user_id=friend_user_id,
            my_tg_id=my_tg_id
        )
        wishes = self.db.get_available_wishes_by_user_id(user_id=friend_user_id)
        if wishes:
            text = WISHES_TOP
            await self.bot.send_message(chat_id=my_tg_id,
                    text=text,
                    reply_markup=None,
                    parse_mode='HTML')
            for wish in wishes:
                wish_id = wish.pop('id')
                text = "\n".join([str(row) for row in wish.values() if row])
                if number_of_wishes_reserved_by_me < 2:
                    reserve_wish_markup = markups.reserve_wish_button(
                        wish_id=wish_id,
                        hashed=hashed
                    )
                else:
                    reserve_wish_markup = None
                await self.bot.send_message(chat_id=my_tg_id,
                                    text=text,
                                    reply_markup=reserve_wish_markup,
                                    parse_mode='HTML')
            user_info = self.db.get_user_info_by_user_id(user_id=friend_user_id)
            if number_of_wishes_reserved_by_me < 2:
                text = FRIEND_WISHES_BOTTOM.format(name=user_info["name"], birthdate=user_info["birthdate"])
            else:
                text = FRIENDS_WISHES_BLOCKED.format(name=user_info["name"], birthdate=user_info["birthdate"])
        else:
            text = FRIEND_WISHES_EMPTY_BOTTOM.format(name=user_info["name"], birthdate=user_info["birthdate"])
        markup = markups.friend_wishlist_markup()
        return dict(text=text, markup=markup)

    async def reserve_wish(self, wish_id, tg_id):
        self.db.reserve_wish(wish_id=wish_id, tg_id_who_chose=tg_id)
        text = '<b>Подарок успешно забронирован!</b>'
        await self.bot.send_message(chat_id=tg_id,
                                    text=text,
                                    reply_markup=None,
                                    parse_mode='HTML')



"""
    async def message_main_menu_buttons_click(self, message):
        text = phrases.phrase_for_answer_to_main_menu_buttons(
            data=dict(
                button_title=message.text
            )
        )
        return dict(text=text)

    async def message_main_menu_button_notification_click(self, message):
        await self.notification.notify_admins_about_some_event(
            data=dict(
                user_name=message.from_user.first_name,
                user_nickname=message.from_user.username,
                date=datetime.now().date,
                time=datetime.now().time,
            )
        )
        text = "Notification has been sent to admins"
        return dict(text=text)
"""
