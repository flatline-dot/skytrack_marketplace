import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path_sqlite_db = os.path.join('.', 'sqlite.db')

engine = create_engine(f'sqlite:///{path_sqlite_db}')
app_session = sessionmaker(bind=engine)

Base = declarative_base()
