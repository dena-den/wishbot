from datetime import datetime
from aiogram import types
from db.db_connector import Database
from const.queries import *
from . import markups
from const import states
import re
from logic import utils
import logging


class Controller:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    async def command_start(self, message, state):
        await state.finish()
        name = message.from_user.first_name
        text = f"Привет, {name}!"
        is_user_exist = self.db.is_user_exist(tg_id=message.from_user.id)
        markup = markups.start_menu_markup(is_user_exist=is_user_exist)
        return dict(text=text, markup=markup)

    async def enter_name(self, message, state):
        text = f"Введите имя"
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
                text = f"Введите дату рождения"
                markup = markups.back_to_markup(to='name')
                await state.set_state(states.User.birthdate)
            elif not len(user_data) < 128:
                text = "Введено слишком длинное имя. Максимальная длина 128 символов.\n" \
                       "Введите имя."
                markup = markups.back_to_markup(to='start')
            else:
                text = "Введено некорректное имя.\n" \
                       "Пожалуйста, используйте только буквы кириллицы или латиницы, тире.\n" \
                       "Введите имя."
                markup = markups.back_to_markup(to='start')
        else:
            text = f"Введите дату рождения"
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
                text = f"Введите номер телефона, если не против."
                markup = markups.back_to_markup(to='birthdate')
                await state.set_state(states.User.phone)
            else:
                text = 'Введена некорректная дата.'
                markup = markups.back_to_markup(to='name')
        else:
            text = f"Введите номер телефона, если не против."
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
            text = "Проверьте корректность введенных данных:\n" \
                   f"{user_data}"
        markup = markups.back_to_markup(to='phone')
        return dict(text=text, markup=markup)

    async def add_user_to_db(self, message, state):
        async with state.proxy() as data:
            user_data = dict(
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
        wishes = self.db.get_wishes_by_tg_id(tg_id=tg_id)
        for wish in wishes:
            wish_id = wish.pop('id')
            delete_button_disabled = bool(wish['is_reserved'])
            add_link_button_disabled = bool(wish['product_link'])
            wish['is_reserved'] = '🔒'if wish['is_reserved'] else '🆓'
            delete_wish_markup = markups.delete_wish_button(
                wish_id=wish_id,
                delete_button_disabled=delete_button_disabled,
                add_link_button_disabled=add_link_button_disabled
            )
            text = "\n".join([str(row) for row in wish.values() if row])
            await self.bot.send_message(chat_id=tg_id,
                                text=text,
                                reply_markup=delete_wish_markup,
                                parse_mode='HTML')
        if wishes:
            text = 'Это твой список подарков.'
        else:
            text = 'Твой список подарков пуст. Их можно добавить с помощью кнопки ниже.'
        markup = markups.my_wishlist_markup()
        return dict(text=text, markup=markup)

    async def enter_wish_name(self, message, state):
        text = 'Введите описание подарка'
        markup = markups.back_to_markup(to='wishlist')
        await state.set_state(states.Wish.wish_name_to_add)
        return dict(text=text, markup=markup)

    async def check_is_user_exist(self, tg_id):
        is_user_exist = self.db.is_user_exist(tg_id=tg_id)
        return is_user_exist

    async def get_wish_name(self, wish_id):
        wish_name = self.db.get_wish_name_by_id(wish_id=wish_id)
        return wish_name

    async def add_wish(self, message, state):
        user_id = self.db.get_user_id_by_tg_id(tg_id=message.from_user.id)
        wishlist_data = dict(
            user_id=user_id,
            name=message.text
        )
        self.db.add_wish(wishlist_data=wishlist_data)

    async def delete_wish(self, wish_id):
        self.db.delete_wish(wish_id=wish_id)

    async def input_wish_link(self, state, wish_id):
        text = 'Вставьте ссылку, которую хотите добавить'
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
        wishes = self.db.get_wishes_reserved_by_me(tg_id=tg_id)
        for wish in wishes:
            wish_id = wish.pop('id')
            text = "\n".join([str(row) for row in wish.values() if row])
            unreserve_wish_markup = markups.unreserve_wish_button(wish_id=wish_id)
            await self.bot.send_message(chat_id=tg_id,
                                text=text,
                                reply_markup=unreserve_wish_markup,
                                parse_mode='HTML')
        text = 'Это список забронированных тобой подарков.'
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
        await state.finish()
        if len(message.text) == 6:
            friend_user_id = int(message.text)
        else:
            friend_user_id = self.db.get_user_id_by_phone(phone=message.text)
        return friend_user_id

    async def display_friends_wishlist(self, my_tg_id, friend_user_id):
        number_of_wishes_reserved_by_me = self.db.how_many_wishes_are_reserved(
            friend_user_id=friend_user_id,
            my_tg_id=my_tg_id
        )
        wishes = self.db.get_available_wishes_by_user_id(user_id=friend_user_id)
        for wish in wishes:
            wish_id = wish.pop('id')
            text = "\n".join([str(row) for row in wish.values() if row])
            if number_of_wishes_reserved_by_me < 2:
                reserve_wish_markup = markups.reserve_wish_button(wish_id=wish_id)
            else:
                reserve_wish_markup = None
            await self.bot.send_message(chat_id=my_tg_id,
                                text=text,
                                reply_markup=reserve_wish_markup,
                                parse_mode='HTML')
        user_info = self.db.get_user_info_by_user_id(user_id=friend_user_id)
        text = f'Это список подарков твоего друга {user_info["name"]}.\n' \
               f'Его день рождения: {user_info["birthdate"]}'
        if number_of_wishes_reserved_by_me >= 2:
            text += f'\n\n<b>Ты уже выбрал 2 подарка для этого друга. ' \
                    f'Оставь другим.</b>'
        markup = markups.friend_wishlist_markup()
        return dict(text=text, markup=markup)

    async def reserve_wish(self, wish_id, tg_id):
        self.db.reserve_wish(wish_id=wish_id, tg_id_who_chose=tg_id)



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
