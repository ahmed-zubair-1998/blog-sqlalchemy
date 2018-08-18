# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from .base import Base


class FlaggedComment(Base):
    __tablename__ = 'flagged_comments'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), primary_key=True)
    def __init__(self, user, comment):
        self.user_id = user
        self.comment_id = comment