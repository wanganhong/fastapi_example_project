#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import logging
from loguru import logger

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 定位到log日志文件
log_path = os.path.join(basedir, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_error = os.path.join(log_path, 'error.log')
log_path_info = os.path.join(log_path, 'info.log')
log_path_debug = os.path.join(log_path, 'debug.log')

custom_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | " \
                "<level>{message}</level>"
logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True, level=logging.ERROR)
logger.add(log_path_info, rotation="20 MB", retention=5, enqueue=True, level=logging.INFO, format=custom_format)
logger.add(log_path_debug, rotation="20 MB", retention=0, enqueue=True, level=logging.DEBUG, format=custom_format)
