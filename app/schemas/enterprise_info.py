#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum


class EnterpriseTypeEnum(str, Enum):
    gy: str = 'GY'  # 国有企业
    my: str = 'MY'  # 民营企业
    qt: str = 'QT'  # 其它企业
