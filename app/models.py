from sqlalchemy import Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship

from .create_engine_db import Base


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    author = Column(String)
    release_date = Column(Date)


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    address = Column(String, unique=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    orders = relationship('Order', backref='user')


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    reg_date = Column(Date)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    orderitems = relationship('Orderitem', backref='order')


class Orderitem(Base):
    __tablename__ = 'orderitem'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('book.id'))
    shop_id = Column(Integer, ForeignKey('shop.id'))
    book_quantity = Column(Integer)
    book = relationship('Book', backref='orderitems')
    shop = relationship('Shop', backref='orderitems')
