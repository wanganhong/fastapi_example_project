#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from typing import List, Union
from urllib.parse import quote_plus

from pydantic import AnyHttpUrl, IPvAnyAddress, BaseSettings


class BaseConfig(BaseSettings):
    DEBUG: bool = False

    # 接口前缀
    API_STR: str = "/api"
    # v1接口前缀
    API_V1_STR: str = f"{API_STR}/v1"
    # SECRET_KEY 记得保密生产环境 不要直接写在代码里面
    SECRET_KEY: str = "qwertyuiopasdfghjklzxcvbnm"

    # jwt加密算法
    JWT_ALGORITHM: str = "HS256"
    # jwt token过期时间 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 根路径
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # 项目信息
    PROJECT_NAME: str = "xxx接口文档"
    DESCRIPTION: str = "example"

    # 跨域
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: List[str] = ['*']

    # sqlite配置
    SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"

    # mongodb配置
    MONGO_USER: str = 'mongodbuser'
    MONGO_PASSWORD: str = '123456'
    MONGO_HOST: Union[AnyHttpUrl, IPvAnyAddress] = '172.16.55.163'
    MONGO_PORT: int = 50010
    MONGO_URI: str = f'mongodb://{MONGO_USER}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}'
    MONGO_DBNAME: str = 'example'

    # mysql配置
    # MYSQL_USERNAME: str = 'root'
    # MYSQL_PASSWORD: str = "Admin12345-"
    # MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "172.16.137.129"
    # MYSQL_DATABASE: str = 'FastAdmin'
    # SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
    #                           f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

    # 内置用户配置
    BUILT_IN_USERNAME = 'admin'
    BUILT_IN_PASSWORD = '123asd!@#$'

    class Config:
        case_sensitive = True
