# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable = False)
    body = Column(String, nullable = False)
    created = Column(DateTime, nullable = False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", backref = "posts")

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author_id = author
        self.created = datetime.now()