#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/18 22:51
@annotation = ''
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

_log_config = [
    ['', '', 'debug'],
    ['error-log', '', 'debug'],
]

log_config = [
    ["order-log", "order.log", "debug"],
    ["sys-log", "sys.log", "debug"],
    ["user-log", "user.log", "debug"],
]


class QuantLoggerFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super(QuantLoggerFormatter, self).__init__(fmt=fmt, datefmt=datefmt, style=style)

    def formatTime(self, record, datefmt=None):

        from quant.environment import Environment
        try:
            dt = Environment.get_instance().calendar_dt.strftime(datefmt)
        except Exception:
            dt = datetime.now().strftime(datefmt)
        return dt


def init_log(log_config=log_config, dir_path='logs'):
    formater = QuantLoggerFormatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s',
                                    '%Y-%m-%d %H:%M:%S', )
    """
    logging.basicConfig(level=logging.DEBUG,
        format='%(name)-12s %(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=log_file,
        filemode='a')
    """
    if not log_config:
        log_config = _log_config
    else:
        log_config = [(n, os.path.join(dir_path, p), l)
                      for n, p, l in log_config]

    for log in log_config:
        logger = logging.getLogger(log[0])
        if log[1]:
            handler = RotatingFileHandler(log[1], 'a', maxBytes=pow(1024, 3), backupCount=2, encoding="utf8")
        else:
            import sys
            handler = logging.StreamHandler(sys.stderr)
            logger.propagate = False
        handler.setFormatter(formater)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, log[2].upper()))


def get(log_name=''):
    return logging.getLogger(log_name)


def error(msg, *args, **kwargs):
    get("cgi-log").error(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    get("cgi-log").warn(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    get("cgi-log").info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    get("cgi-log").debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    get("cgi-log").log(level, msg, *args, **kwargs)


sys_log = get('sys-log')
order_log = get('order-log')
user_log = get('user-log')
