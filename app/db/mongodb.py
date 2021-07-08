#!/usr/bin/env python
# -*- coding:utf-8 -*-

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import config


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database():
    return db.client[config.MONGO_DBNAME]


async def get_client() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logger.info("Connect mongodb...")
    db.client = AsyncIOMotorClient(config.MONGO_URI)
    logger.info("Connect mongodb success.")


async def close_mongo_connection():
    logger.info("Close mongodb...")
    db.client.close()
    logger.info("Close mongodb success.")
