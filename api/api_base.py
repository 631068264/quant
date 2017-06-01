#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/22 09:32
@annotation = ''
"""
from model.const import FREQUENCY
from model.environment import Environment

__all__ = []


def export_as_api(func):
    __all__.append(func.__name__)
    return func


@export_as_api
def get_open_orders():
    """
    获取当日未成交订单数据

    :return: List[:class:`~Order` object]
    """
    return Environment.get_instance().broker.get_open_orders()


@export_as_api
def cancel_order(order):
    """
    撤单

    :param order: 需要撤销的order对象
    :type order: :class:`~Order` object
    """
    if order is not None:
        env = Environment.get_instance()
        if env.can_cancel_order(order):
            env.broker.cancel_order(order)
        return order


@export_as_api
def history(symbol, bar_count, frequency=None, fields=None):
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
    if frequency is None:
        frequency = env.config.base.frequency
    if frequency not in FREQUENCY.ALL:
        return None
    if fields is None:
        fields = env.data_proxy.valid_fields
    dt = env.calendar_dt
    return env.data_proxy.history(symbol, frequency, bar_count, dt, fields)


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
    :return: list[`datetime.datetime`]
    """
    return Environment.get_instance().get_calendar(symbol, frequency, start_date, end_date)


@export_as_api
def get_previous_date(symbol, frequency, dt, n=1):
    return Environment.get_instance().get_previous_date(symbol, frequency, dt, n=n)


@export_as_api
def get_next_date(symbol, frequency, dt):
    return Environment.get_instance().get_next_date(symbol, frequency, dt)


@export_as_api
def plot(series_name, value):
    # Environment.get_instance().add_plot(series_name, value)
    pass
