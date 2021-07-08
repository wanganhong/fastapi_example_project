#!/usr/bin/env python
# -*- coding:utf-8 -*-


from fastapi import FastAPI, Depends
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.core.config import config
from app.core.error_handlers import (
    request_validation_error_handler,
    http_exception_handler,
    unknown_exception_handler
)
from app.core.security import check_jwt_token
from app.db.mongodb import connect_to_mongo, close_mongo_connection


def create_app():
    app = FastAPI(
        title=config.PROJECT_NAME,
        description=config.DESCRIPTION,
        docs_url=None,
        redoc_url=None
    )

    # 跨域设置
    register_cors(app)
    # 注册事件处理方法
    register_event_handler(app)
    # 处置异常处理方法
    register_exception_handler(app)

    if config.DEBUG:
        # 注册静态文件
        register_static_file(app)
        # 注册接口文档
        register_swagger_docs(app)

    # 注册路由
    register_router(app)
    return app


def register_router(app: FastAPI, is_auth: bool = True):
    """
    路由注册
    :param app:
    :param is_auth: 是否加入认证
    :return:
    """
    # 注册与认证
    if is_auth:
        from app.api.authenticaion import router as auth_router
        app.include_router(auth_router,
                           prefix=config.API_STR)
    # Api v1
    from app.api.v1 import api_router as api_router_v1
    if is_auth:
        dependencies = [Depends(check_jwt_token)]
    else:
        dependencies = None
    app.include_router(api_router_v1,
                       prefix=config.API_V1_STR,
                       dependencies=dependencies)


def register_cors(app: FastAPI):
    """
    支持跨域
    :param app:
    :return:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_static_file(app: FastAPI):
    """
    挂载静态文件
    :param app:
    :return:
    """
    app.mount('/static', StaticFiles(directory=f'{config.BASE_DIR}/static'), name='static')


def register_event_handler(app: FastAPI):
    """
    设置事件处理
    :param app:
    :return:
    """
    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)


def register_exception_handler(app: FastAPI):
    """
    设置异常处理
    :param app:
    :return:
    """
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)


def register_swagger_docs(app: FastAPI):
    """
    设置加载本地资源的swagger docs接口文档
    :param app:
    :return:
    """

    @app.get('/docs', include_in_schema=False)
    async def get_custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url='/static/swagger-ui/swagger-ui-bundle.js',
            swagger_css_url='/static/swagger-ui/swagger-ui.css',
            swagger_favicon_url='/static/swagger-ui/favicon.png'
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_url_redirect():
        return get_swagger_ui_oauth2_redirect_html()
