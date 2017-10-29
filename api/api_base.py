#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/22 09:32
@annotation = ''
"""

from quant import Environment

__all__ = [
    "Environment",
]


def register_api(name, func):
    globals()[name] = func
    __all__.append(name)


def export_as_api(func):
    __all__.append(func.__name__)
    globals()[func.__name__] = func
    return func


@export_as_api
def get_open_orders(symbol=None):
    """
    获取当日未成交订单数据
    """
    return Environment.get_instance().broker.get_open_orders(symbol)


@export_as_api
def cancel_order(order):
    """
    撤单
    """
    if order is None:
        raise KeyError("cancel order fail {order}".format(order=order))
    env = Environment.get_instance()
    if env.can_cancel_order(order):
        env.broker.cancel_order(order)
    return order


@export_as_api
def history(symbol, bar_count, frequency=None, field=None):
    """
    返回K线行情
    =========================   ===================================================
    fields                      字段名
    =========================   ===================================================
    datetime                    时间戳
    open                        开盘价
    high                        最高价
    low                         最低价
    close                       收盘价
    volume                      成交量
    =========================   ===================================================
    """
    env = Environment.get_instance()
    dt = env.calendar_dt
    return env.history(symbol, frequency, bar_count, dt, field)


@export_as_api
def instruments(symbols):
    """
    返回交易所/币种信息
    """
    return Environment.get_instance().get_instrument(symbols)


@export_as_api
def get_trade_date(symbol, frequency, start_date, end_date):
    """
    交易时间
    """
    return Environment.get_instance().get_calendar(symbol, frequency, start_date, end_date)


@export_as_api
def get_previous_date(symbol, frequency, dt, n=1):
    return Environment.get_instance().get_previous_date(symbol, frequency, dt, n=n)


@export_as_api
def get_next_date(symbol, frequency, dt, n=1):
    return Environment.get_instance().get_next_date(symbol, frequency, dt, n=n)


@export_as_api
def plot(series_name, value):
    Environment.get_instance().add_plot(series_name, value)
