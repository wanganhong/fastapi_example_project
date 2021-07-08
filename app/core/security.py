#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Optional
from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, PyJWTError
from fastapi import Header
from pydantic import ValidationError

from app.core.errors import UserTokenError
from app.core.config import config

try:
    import bcrypt
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def verify_password(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(password):
        return pwd_context.hash(password)
except ImportError:
    from werkzeug.security import (
        generate_password_hash as get_password_hash,
        check_password_hash as verify_password
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(exp=expire)
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def check_jwt_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.JWT_ALGORITHM)
        return payload
    except (PyJWTError, ExpiredSignatureError, ValidationError):
        raise UserTokenError(detail='Invalid access token.')
