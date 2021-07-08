#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from typing import Callable
from uuid import uuid4

from fastapi import Response, Request
from fastapi.routing import APIRoute

from loguru import logger


class ContextIncludedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """请求日志记录"""
            logger.info(f'{request.client[0]} -- "{request.method} {request.scope["path"]} '
                        f'{request.scope["type"]}/{request.scope["http_version"]}"')
            query_string = request.scope['query_string'].decode()
            if query_string:
                logger.debug(f'?{query_string}')

            body = await request.body()
            if body:
                logger.debug(body.decode())

            start_time = time.time()
            request_id = str(uuid4())
            response: Response = await original_route_handler(request)
            response.headers["Request-ID"] = request_id
            response.headers['X-Process-Time'] = str(time.time() - start_time)

            return response

        return custom_route_handler
