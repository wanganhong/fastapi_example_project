#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


config = DevelopmentConfig()
