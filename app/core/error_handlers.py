#!/usr/bin/env python
# -*- coding:utf-8 -*-

from loguru import logger
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException


async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    message = ""
    for error in exc.errors():
        message += ".".join(error.get("loc")) + ":" + error.get("msg") + ";"

    logger.error(f'RequestValidationError "{request.method} {request.url}", Message: {message}')
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={'code': status.HTTP_400_BAD_REQUEST, 'message': message})


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f'HttpException "{request.method} {request.url}", Message: {exc.detail}')
    return JSONResponse(status_code=exc.status_code,
                        content={'code': exc.status_code, 'message': exc.detail})


async def unknown_exception_handler(request: Request, exc: Exception):
    logger.exception(f'UnknownException "{request.method} {request.url}", Message: {str(exc)}')
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': "Server Error"})
