import sqlalchemy as database
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.elements import and_, or_
from .models import *
from os import getenv
from sqlalchemy import select, Column, Integer, String, ForeignKey, Boolean, DateTime, SmallInteger, Text, DECIMAL, text, func
from random import randint


class Database:
    def __init__(self):
        engine = database.create_engine(getenv("DATABASE"))
        self.session = scoped_session(sessionmaker(bind=engine))

    def is_user_exist(self, tg_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id) \
                    .where(User.tg_id.__eq__(tg_id))) \
                    .scalar()
                return bool(query)

    def get_user_id(self, tg_id):
        with self.session() as session:
            with session.begin():
                query = session \
                    .execute(select(User.id) \
                    .where(User.tg_id.__eq__(tg_id))) \
                    .scalar()
                return query

    def get_wishes(self, tg_id):
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
                print(query)
                return [dict(row) for row in query if query]

    def add_user(self, user_data):
        with self.session() as session:
            with session.begin():
                #while True:
                user_data['id'] = randint(100000, 999999)
                data = User(**user_data)
                session.add(data)
                    # try:
                    #     session.add(data)
                    #     break
                    # except IntegrityError:
                    #     print('IntegrityError')
                    #     continue

    def add_gift(self, wishlist_data):
        with self.session() as session:
            with session.begin():
                data = Wishlist(**wishlist_data)
                session.add(data)

    def del_gift(self, gift_id):
        with self.session() as session:
            with session.begin():
                session.query(Wishlist)\
                .where(Wishlist.id.__eq__(gift_id))\
                .update({Wishlist.is_active: 0})
