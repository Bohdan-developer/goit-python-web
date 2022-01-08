from sqlalchemy import (ForeignKey, Column, Integer, String, Unicode, Table)
from sqlalchemy.orm import relationship
from db import engine, Base


class Contact(Base):
    __tablename__ = 'contacts'
    contact_id = Column("contact_id",Integer, primary_key=True, autoincrement=True)
    name = Column("name",Unicode(50), nullable=False)
    phones_rel = relationship('Phone', backref='contacts', cascade="all, delete, delete-orphan")
    emails_rel = relationship('Email', backref='contacts', cascade="all, delete, delete-orphan")
    birthdays_rel = relationship('Birthday', backref='contacts', cascade="all, delete, delete-orphan")
    address_rel = relationship('Address', backref='contacts', cascade="all, delete, delete-orphan")


class Phone(Base):
    __tablename__ = 'phones'
    phone_id = Column("phone_id", Integer, primary_key=True)
    contact_id = Column("contact_id", Integer, ForeignKey("contacts.contact_id"), nullable=False)
    phone = Column("phone", String(50))


class Email(Base):
    __tablename__ = 'emails'
    email_id = Column("email_id", Integer, primary_key=True)
    contact_id = Column("contact_id", Integer, ForeignKey("contacts.contact_id"), nullable=False)
    email = Column("email", String(50))


class Birthday(Base):
    __tablename__ = "birthdays"
    birthday_id = Column("birthday_id", Integer, primary_key=True)
    contact_id = Column("contact_id", Integer, ForeignKey("contacts.contact_id"), nullable=False)
    birthday = Column("birthday", String(50))


class Address(Base):
    __tablename__ = "address"
    address_id = Column("address_id", Integer, primary_key=True)
    contact_id = Column("contact_id", Integer, ForeignKey("contacts.contact_id"), nullable=False)
    address = Column("address", String(50))


Base.metadata.create_all(engine)
