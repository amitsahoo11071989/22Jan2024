from sqlalchemy import Boolean, Column, Integer, String, func, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime
from sqlalchemy.sql.expression import text

from .database import Base


class IntegrityError(Exception):
    def __init__(self, name: str):
        self.name = name


class Users(Base):
    __tablename__ = "users"

    #id = Column(Integer, primary_key=True, nullable=False)
    email_id = Column(String, nullable=False, unique=True, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=True)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    creator_email = Column(String, ForeignKey('users.email_id'), nullable=False)



