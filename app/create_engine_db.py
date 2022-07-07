import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path_sqlite_db = os.path.join('.', 'sqlite.db')

SQL_DATABASE_URL = f'sqlite:///{path_sqlite_db}'

engine = create_engine(SQL_DATABASE_URL)

app_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
