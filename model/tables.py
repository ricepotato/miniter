from sqlalchemy.orm import relationship


from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, FLOAT, DATETIME, SMALLINT
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(100))
    profile = Column(String(50))

    tweets = relationship("Tweet", back_populates="user")


class Follow(Base):
    __tablename__ = "user_follow_list"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    follow_id = Column(Integer)


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    tweet = Column(String(300))

    user = relationship("User", back_populates="tweets")