#!/usr/bin/env python
# -*- coding:utf-8 -*-


from fastapi import Query, Path, APIRouter
from fastapi.responses import JSONResponse

from app.crud import enterprise_info
from app.core import response_status
from app.core.custom_routing import ContextIncludedRoute
from app.schemas.enterprise_info import *

router = APIRouter(route_class=ContextIncludedRoute)


@router.get('/enterprise_info/', summary='企业--列表查询')
async def get_enterprise_infos(
        gt_id: str = Query(None, description='指定id最小值大于某个值，首次不传,后面每次从上轮查询中最后一条记录的_id字段获取'),
        enterprise_type: EnterpriseTypeEnum = Query(None, description='企业类型（性质）'),
        size: int = Query(10, ge=1)
):
    total, records = await enterprise_info.get_enterprise_info(gt_id, enterprise_type, size)
    return response_status.resp_200(data={'records': records, 'total': total})


@router.get('/enterprise_info/{id}/', summary='企业--根据id查询')
async def get_enterprise_info(id: str = Path(..., description='指定要获取的记录的id（实际使用数据中_id字段的值）')):
    data = await enterprise_info.get_enterprise_info_by_id(id)
    if data is None:
        return JSONResponse(status_code=404, content={'code': 404, 'message': 'Item not found'})
    return response_status.resp_200(data=data)
