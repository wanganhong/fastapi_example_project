#!/usr/bin/env python
# -*- coding:utf-8 -*-


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sqlite import get_db
from app.core import response_status
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserLoginForm, UserRegisterForm

router = APIRouter(tags=['用户注册认证相关接口'])


@router.post('/login/', summary='登录')
def login(form: UserLoginForm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if user:
        if verify_password(user.password, form.password):
            token = create_access_token({'username': form.username})
            return response_status.resp_200(data={'token': token}, message='Login success')
    return response_status.resp_400(message="Incorrect username or password")


@router.post('/register/', summary='注册')
def register(form: UserRegisterForm, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if user:
        return response_status.resp_400(message=f"User: username='{form.username}', already exist")
    u = User(username=form.username,
             password=get_password_hash(form.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return response_status.resp_201(message='Register success')


@router.get('/users/', summary='查看已有用户信息')
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    data = [{'id': user.id, 'username': user.username} for user in users]
    return response_status.resp_200(data=data)
