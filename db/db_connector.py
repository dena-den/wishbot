import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.elements import and_, or_
from .models import *
from os import getenv
from sqlalchemy import select, Column, Integer, String, ForeignKey, Boolean, DateTime, SmallInteger, Text, DECIMAL, text, func
from const.queries import *
from logic.utils import get_moscow_datetime
from logic import memory


class Database:
    def __init__(self):
        engine = sqlalchemy.create_engine(getenv("DATABASE"))
        self.session = scoped_session(sessionmaker(bind=engine))

    def get_all_user_ids(self):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id)) \
                    .fetchall()
                return [row['id'] for row in query if query]

    def is_user_exist(self, tg_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id) \
                    .where(User.tg_id.__eq__(tg_id))) \
                    .scalar()
                return bool(query)

    def get_user_id_by_tg_id(self, tg_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id) \
                    .where(User.tg_id.__eq__(tg_id))) \
                    .scalar()
                return query

    def get_tg_id_by_user_id(self, user_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.tg_id) \
                    .where(User.id.__eq__(user_id))) \
                    .scalar()
                return query

    def get_user_id_by_phone(self, phone):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id) \
                    .where(User.phone.__eq__(phone))) \
                    .scalar()
                return query

    def get_user_info_by_user_id(self, user_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.name, User.birthdate) \
                    .where(User.id.__eq__(user_id))) \
                    .fetchone()
                return query

    def get_wish_name_by_id(self, wish_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(Wishlist.name) \
                    .where(Wishlist.id.__eq__(wish_id))) \
                    .scalar()
                return query

    def get_wishes_by_tg_id(self, tg_id):
        with self.session() as session:
            with session.begin():
                user_id = session \
                    .execute(select(User.id) \
                    .where(User.tg_id.__eq__(tg_id))) \
                    .scalar()
                query = session \
                    .execute(select(Wishlist.id, Wishlist.name, Wishlist.image_link, Wishlist.product_link, Wishlist.is_reserved) \
                    .where(and_(Wishlist.user_id.__eq__(user_id), Wishlist.is_active.__eq__(1)))) \
                    .fetchall()
                return [dict(row) for row in query if query]

    def get_available_wishes_by_user_id(self, user_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(Wishlist.id, Wishlist.name, Wishlist.image_link, Wishlist.product_link) \
                    .where(and_(Wishlist.user_id.__eq__(user_id),
                                Wishlist.is_active.__eq__(1),
                                Wishlist.is_reserved.__eq__(0)))) \
                    .fetchall()
                return [dict(row) for row in query if query]

    def get_wishes_reserved_by_me(self, tg_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(QUERY_WISHES_RESERVED_BY_ME.format(tg_id=tg_id)) \
                    .fetchall()
                return [dict(row) for row in query if query]


    def add_user(self, user_data):
        with self.session() as session:
            with session.begin():
                data = User(**user_data)       
                session.add(data)


    def add_wish(self, wishlist_data):
        with self.session() as session:
            with session.begin():
                data = Wishlist(**wishlist_data)
                session.add(data)

    def add_wish_link(self, wish_id, link):
        with self.session() as session:
            with session.begin():
                session.query(Wishlist)\
                .where(Wishlist.id.__eq__(wish_id))\
                .update({Wishlist.product_link: link})

    def delete_wish(self, wish_id):
        with self.session() as session:
            with session.begin():
                session.query(Wishlist)\
                .where(Wishlist.id.__eq__(wish_id))\
                .update({Wishlist.is_active: 0})

    def how_many_wishes_are_reserved(self, friend_user_id, my_tg_id):
        with self.session() as session:
            with session.begin():
                number_of_wishes = session \
                    .execute(QUERY_HOW_MANY_WISHES_ARE_RESERVED.format(
                        friend_user_id=friend_user_id,
                        my_tg_id=my_tg_id
                    )).scalar()
                return number_of_wishes

    def reserve_wish(self, wish_id, tg_id_who_chose):
        with self.session() as session:
            with session.begin():
                session.query(Wishlist)\
                .where(Wishlist.id.__eq__(wish_id))\
                .update({Wishlist.is_reserved: 1})

                data = WishHistory(
                    wish_id=wish_id,
                    tg_id_who_chose=tg_id_who_chose
                )
                session.add(data)

    def unreserve_wish(self, wish_id, tg_id_who_chose):
        with self.session() as session:
            with session.begin():
                session.query(WishHistory)\
                .where(and_(WishHistory.wish_id.__eq__(wish_id),
                            WishHistory.tg_id_who_chose.__eq__(tg_id_who_chose)))\
                .update({WishHistory.end_datetime: get_moscow_datetime()})

                session.query(Wishlist)\
                .where(Wishlist.id.__eq__(wish_id))\
                .update({Wishlist.is_reserved: 0})
