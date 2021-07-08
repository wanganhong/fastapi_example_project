#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app.core.utils import get_object_id, serialize_mongo_doc
from app.db.mongodb import get_database

coll_name = 'enterprise_info'


async def get_enterprise_info(gt_id, enterprise_type, size):
    db = await get_database()
    query = {}
    if enterprise_type is not None:
        query.update(enterprise_type=enterprise_type)

    total = await db[coll_name].count_documents(query)

    if gt_id is not None:
        query.update(_id={'$gt': get_object_id(gt_id)})

    data = []
    async for row in db[coll_name].find(query).limit(size):
        data.append(serialize_mongo_doc(row))
    return total, data


async def get_enterprise_info_by_id(id_):
    db = await get_database()
    oid = get_object_id(id_)
    if oid is not None:
        item = await db[coll_name].find_one({'_id': oid})
    else:
        item = None
    return serialize_mongo_doc(item) if item else None
