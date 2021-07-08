#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os

"""
根据是否设置ENV环境变量确定具体选用的配置：
    1. 已设置，选取生产环境配置
    2. 未设置，选取开发环境配置
"""
env = os.getenv('ENV')

if env:
    from .production_config import config
else:
    from .development_config import config
