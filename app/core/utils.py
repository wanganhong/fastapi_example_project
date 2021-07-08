#!/usr/bin/env python
# -*- coding:utf-8 -*-


from bson import ObjectId
from bson.errors import InvalidId


def serialize_mongo_doc(doc: dict):
    for name, value in doc.items():
        if name == '_id':
            doc[name] = str(value)
    return doc


def get_object_id(id_):
    if id_ is None:
        return None

    try:
        oid = ObjectId(id_)
    except InvalidId:
        oid = None
    return oid
