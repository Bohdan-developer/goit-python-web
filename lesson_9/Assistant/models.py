from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer, String, Unicode,
    Table
)
from sqlalchemy.orm import relationship

from db import  engine, Base


class Contact(Base):
    __tablename__ = 'contacts'
    contact_id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))
    birthday = Column(Unicode(10))


    #
    # phones_rel = relationship('Phone', back_populates='contact_rel')
    #
    # emails_rel = relationship('Email', back_populates='contact_rel')


class Phone(Base):
    __tablename__ = 'phones'
    phone_id = Column(Integer, primary_key=True)
    phone = Column(String(50))

    contact_id = Column(Integer, ForeignKey("contacts.contact_id"))

    contact_phone_id = relationship("Contact", foreign_keys=[contact_id])
    # contact_id = Column(Integer, ForeignKey('Contact.contact_id', ondelete='CASCADE'), nullable=False)
    # contact_rel = relationship('Contact', back_populates='phones_rel')


class Email(Base):
    __tablename__ = 'emails'
    email_id = Column( ForeignKey("contacts.contact_id"), primary_key=True)
    email = Column(String(50))

    # contact_id= Column(Integer, ForeignKey("contacts.contact_id"))
    # contact_email_id = relationship("Contact", foreign_keys=[contact_id])


Base.metadata.create_all(engine)
