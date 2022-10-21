from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime, Boolean, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from logic.utils import get_moscow_datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    phone = Column(String, nullable=True)
    tg_id = Column(BigInteger, nullable=False)
    tg_nickname = Column(String, nullable=False)
    registration_datetime = Column(DateTime, default=get_moscow_datetime())
    is_admin = Column(Boolean, default=False)


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    image_link = Column(String, nullable=True)
    product_link = Column(String, nullable=True)
    is_reserved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class WishHistory(Base):
    __tablename__ = "wish_histories"
    id = Column(Integer, primary_key=True)
    tg_id_who_chose = Column(BigInteger, nullable=False)
    gift_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, default=None)
