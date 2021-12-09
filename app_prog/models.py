from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Table,
    Text,
    PrimaryKeyConstraint,
    VARCHAR,
    create_engine)
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine("mysql://root:12345@localhost/aplabs")
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    firstName = Column(String(32), nullable=False)
    lastName = Column(String(32), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    phone = Column(String(32), nullable=False, unique=True)
    city = Column(String(32), nullable=False)


class Announcement(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, primary_key=True)
    tittle = Column(String(32), nullable=False)
    content = Column(String(256), nullable=False)
    authorid = Column(Integer, ForeignKey('user.id'))
    users = relationship('User')


class Local(Base):
    __tablename__ = 'local'
    id = Column(Integer, primary_key=True)
    announcementid = Column(Integer, ForeignKey('announcement.id'))
    announcements = relationship('Announcement')


class Public(Base):
    __tablename__ = 'public'
    id = Column(Integer, primary_key=True)
    announcementid = Column(Integer, ForeignKey('announcement.id'))
    announcements = relationship('Announcement')
