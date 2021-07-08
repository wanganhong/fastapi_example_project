#!/usr/bin/env python
# -*- coding:utf-8 -*-


from sqlalchemy import Column, String, DateTime, Integer

from app.db.sqlite import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    is_active = Column(Integer)
    create_time = Column(DateTime)
