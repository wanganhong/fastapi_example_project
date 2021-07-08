#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from typing import Union

from pydantic import AnyHttpUrl, IPvAnyAddress

from .base_config import BaseConfig


class ProductionConfig(BaseConfig):
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'qwertyuiopasdfghjklzxcvbnm')

    # mongodb配置
    MONGO_USER: str = os.getenv('MONGO_USER', 'mongodbuser')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD', '123asd!@#$')
    MONGO_HOST: Union[AnyHttpUrl, IPvAnyAddress] = os.getenv('MONGO_HOST', '127.0.0.1')
    MONGO_PORT: int = os.getenv('MONGO_PORT', 50010)

    # 内置用户配置
    BUILT_IN_USERNAME = os.getenv('BUILT_IN_USERNAME', 'admin')
    BUILT_IN_PASSWORD = os.getenv('BUILT_IN_PASSWORD', '123asd!@#$')


config = ProductionConfig()
