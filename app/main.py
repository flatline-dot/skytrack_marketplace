from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .models import User, Order, Orderitem
from .schemas import UserSchema, OrderSchema, OrderCreateSchema, OrderSaveSchema
from .dependencies import get_db


app = FastAPI()


@app.get(
    '/user/{user_id}', response_model=UserSchema,
    tags=['user'],
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"msg": "User not found"}
                }
            }
        }
    }
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get(
    '/user/{user_id}/orders',
    tags=['user'],
    response_model=List[OrderSchema],
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"msg": "User not found"}
                }
            }
        }
    }
)
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


@app.post(
    '/order',
    response_model=OrderSaveSchema,
    tags=['order'],
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"msg": "User not found"}
                }
            }
        }
    }
)
def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    order_data = order.dict()
    orderitems_list = []
    db.begin()
    user = db.query(User).filter(User.id == order_data['user_id']).first()
    if user:
        try:
            order = Order(reg_date=order_data['reg_date'], user_id=order_data['user_id'])
            db.add(order)
            db.flush()

            for orderitem in order_data['orderitems']:
                item = Orderitem(**orderitem, order_id=order.id)
                db.add(item)
                db.flush()
                orderitems_list.append(item)
            db.commit()
            order.orderitems = orderitems_list
            return order
        except Exception:
            db.rollback()
            raise HTTPException(status_code=422, detail={"description": "Data entry error"})
    else:
        raise HTTPException(status_code=404, detail={"description": "User not found"})


@app.get(
    '/order/{order_id}',
    response_model=OrderSaveSchema,
    tags=['order'],
    responses={
        404: {
            "description": "Order not found",
            "content": {
                "application/json": {
                    "example": {"msg": "Order not found"}
                }
            }
        }
    }

)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail={"description": "Order not found"})
    return order
