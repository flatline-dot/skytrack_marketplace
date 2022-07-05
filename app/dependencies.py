from .create_engine_db import app_session


def get_db():
    db = app_session()
    try:
        yield db
    finally:
        db.close()
