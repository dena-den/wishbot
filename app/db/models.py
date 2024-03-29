from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime, Boolean, BigInteger
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    phone = Column(String, nullable=True)
    tg_id = Column(BigInteger, nullable=False)
    tg_nickname = Column(String, nullable=True)
    registration_datetime = Column(DateTime, nullable=True)
    is_admin = Column(Boolean, default=False)


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    image_link = Column(String, nullable=True)
    product_link = Column(String, nullable=True)
    is_reserved = Column(Boolean, default=False)


class WishHistory(Base):
    __tablename__ = "wish_histories"
    id = Column(Integer, primary_key=True)
    tg_id_who_chose = Column(BigInteger, nullable=False)
    wish_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, default=None)


class LastViewed(Base):
    __tablename__ = "last_viewed"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    friend_user_id = Column(Integer, primary_key=True)
    view_datetime = Column(DateTime, default=None)


class KeyboardHash(Base):
    __tablename__ = "keyboard_hash"
    tg_id = Column(BigInteger, primary_key=True)
    hash = Column(BigInteger, nullable=True)
