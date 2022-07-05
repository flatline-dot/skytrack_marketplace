from typing import List
from datetime import date
from pydantic import BaseModel


class UserSchema(BaseModel):
    firstname: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class OrderitemBaseSchema(BaseModel):
    book_id: int
    shop_id: int
    book_quantity: int


class OrderitemCreateSchema(OrderitemBaseSchema):
    id: int

    class Config:
        orm_mode = True


class OrderBaseSchema(BaseModel):
    reg_date: date
    user_id: int

    class Config():
        orm_mode = True


class OrderSchema(OrderBaseSchema):
    id: int


class OrderCreateSchema(OrderBaseSchema):
    orderitems: List[OrderitemBaseSchema]


class OrderSaveSchema(OrderSchema):
    orderitems: List[OrderitemCreateSchema]
