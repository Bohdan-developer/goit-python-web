from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

_CONNECTION = 'sqlite:///AddressBook.db'





engine = create_engine(_CONNECTION)


if not "AddressBook.db" :
    con = sqlite3.connect('AddressBook.db')
    print("create db")



Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()
