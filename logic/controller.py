from datetime import datetime
from aiogram import types
from db.db_connector import Database
from const.const import *
from . import markups
from const import states


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
        if not message.text.startswith('Назад'):
            async with state.proxy() as data:
                data['name'] = message.text
        text = f"Введите дату рождения"
        markup = markups.back_to_markup(to='name')
        await state.set_state(states.User.birthdate)
        return dict(text=text, markup=markup)

    async def enter_phone(self, message, state):
        if not message.text.startswith('Назад'):
            async with state.proxy() as data:
                data['birthdate'] = datetime.strptime(message.text, r'%d.%m.%Y').date()
        text = f"Введите номер телефона, если не против"
        markup = markups.back_to_markup(to='birthdate')
        await state.set_state(states.User.phone)
        return dict(text=text, markup=markup)

    async def check_data(self, message, state):
        async with state.proxy() as data:
            if message.text == 'Не хочу сообщать':
                data['phone'] = None
            else:
                data['phone'] = message.text
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

    async def check_is_user_exist(self, tg_id):
        is_user_exist = self.db.is_user_exist(tg_id=tg_id)
        return is_user_exist

    async def display_my_wishlist(self, message, state):
        await state.finish()
        wishes = self.db.get_wishes(tg_id=message.from_user.id)
        for wish in wishes:
            wish_id = wish.pop('id')
            wish['is_reserved'] = '🔒' if wish['is_reserved'] else '🆓'
            text = "\n".join([str(row) for row in wish.values() if row])
            del_gift_markup = markups.delete_wish_button(id=wish_id, name=wish['name'])
            await message.reply(text=text,
                                reply_markup=del_gift_markup,
                                parse_mode='HTML',
                                reply=False)
        text = ''
        markup = markups.my_wishlist_markup()
        return dict(text=text, markup=markup)

    async def enter_wish_name(self, message, state):
        text = 'Введите описание подарка'
        markup = markups.back_to_markup(to='wishlist')
        await state.set_state(states.Wish.wish_name_to_add)
        return dict(text=text, markup=markup)        

    async def add_wish(self, message, state):
        user_id = self.db.get_user_id(tg_id=message.from_user.id)
        wishlist_data = dict(
            user_id=user_id,
            name=message.text
        )
        self.db.add_gift(wishlist_data=wishlist_data)
        

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