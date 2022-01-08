from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

_CONNECTION = 'sqlite:///lesson_9/AddressBook_db'

engine = create_engine(_CONNECTION)

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()
