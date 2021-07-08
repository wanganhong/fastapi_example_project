#!/usr/bin/env python
# -*- coding:utf-8 -*-

from fastapi import status
from fastapi.exceptions import HTTPException


class UserTokenError(HTTPException):
    def __init__(self, detail: str = '用户认证异常'):
        super(UserTokenError, self).__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
