# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from .base import Base


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable = False)
    created = Column(DateTime, nullable = False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", backref='commnets')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", backref='comment_id')

    def __init__(self, body, author, post):
        self.body = body
        self.author_id = author
        self.post_id = post
        self.created = datetime.now()