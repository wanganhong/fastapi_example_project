#!/usr/bin/env python
# -*- coding:utf-8 -*-


from fastapi import APIRouter

from . import enterprise_info

api_router = APIRouter()

api_router.include_router(enterprise_info.router,
                          prefix="/data_assets",
                          tags=['业务接口'])
