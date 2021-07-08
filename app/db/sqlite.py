#!/usr/bin/env python
# -*- coding:utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import config
from app.core.security import get_password_hash

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from app.models import user

# 清空数据库表
for table in Base.metadata.sorted_tables:
    try:
        engine.execute(table.delete())
    except:
        pass

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 增加内置用户
u = user.User(username=config.BUILT_IN_USERNAME,
              password=get_password_hash(config.BUILT_IN_PASSWORD))
session = SessionLocal()
session.add(u)
session.commit()
session.close()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
