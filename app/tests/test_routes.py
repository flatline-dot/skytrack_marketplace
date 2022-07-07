import os
from datetime import date

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import Base, User, Order, Orderitem, Book, Shop
from ..main import app
from ..dependencies import get_db

SQLACHEMY_DATABASE_URL = os.path.join('sqlite:///', '.', 'test_sqlite.db')

engine = create_engine(SQLACHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def get_test_db():
        try:
            db = testing_session()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def fake_data():
    test_db = testing_session()
    test_db.begin()
    user = User(firstname='Victor', last_name='Sokolov', email='sokolov@example.com')
    book = Book(name='Learn Python', author='Mark Lutc', release_date=date.today())
    shop = Shop(name='Ozon', address='Tverskaya 10')

    test_db.add(user)
    test_db.add(book)
    test_db.add(shop)
    test_db.flush()

    order = Order(reg_date=date.today(), user_id=user.id)
    test_db.add(order)
    test_db.flush()

    orderitem = Orderitem(order_id=order.id, book_id=book.id, shop_id=shop.id, book_quantity=10)
    test_db.add(orderitem)
    test_db.commit()


def test_main(client):
    response = client.get('/')
    assert response.status_code == 404


def test_get_user(client, fake_data):
    response = client.get('/user/1')
    data = response.json()
    assert data['email'] == 'sokolov@example.com'
    response = client.get('/user/2')
    data = response.json()
    assert response.status_code == 404
    assert data == {'detail': 'User not found'}


def test_user_orders(client, fake_data):
    response = client.get('/user/1/orders')
    data = response.json()
    assert response.status_code == 200
    assert data == [{'id': 1, 'user_id': 1, 'reg_date': str(date.today())}]
    response = client.get('/user/2/orders')
    data = response.json()
    assert response.status_code == 404
    assert data == {'detail': 'User not found'}


def test_create_order(client, fake_data):
    response = client.post(
        '/order',
        json={
            "reg_date": str(date.today()),
            "user_id": "1",
            "orderitems": [
                {
                    "book_id": "1",
                    "shop_id": "1",
                    "book_quantity": "15"

                }
            ]
        }
    )
    data = response.json()
    assert data == {
                        "id": 2,
                        "reg_date": str(date.today()),
                        "user_id": 1,
                        "orderitems": [
                            {
                                "id": 2,
                                "book_id": 1,
                                "shop_id": 1,
                                "book_quantity": 15
                            }
                        ]
                    }

    response = client.post(
        '/order',
        json={
            "reg_date": str(date.today()),
            "user_id": "2",
            "orderitems": [
                {
                    "book_id": "1",
                    "shop_id": "1",
                    "book_quantity": "15"

                }
            ]
        }
    )

    data = response.json()
    assert response.status_code == 404
    assert data == {'detail': 'User not found'}


def test_get_orders(client, fake_data):
    response = client.get('/order/1')
    data = response.json()
    assert response.status_code == 200
    assert data == {
                        "id": 1,
                        "reg_date": str(date.today()),
                        "user_id": 1,
                        "orderitems": [
                            {
                                "id": 1,
                                "book_id": 1,
                                "shop_id": 1,
                                "book_quantity": 10
                            }
                        ]
                    }

    response = client.get('/order/2')
    data = response.json()
    assert response.status_code == 404
    assert data == {'detail': 'Order not found'}
