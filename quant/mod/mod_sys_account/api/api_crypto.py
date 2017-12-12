#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/22 10:51
@annotation = ''
"""
from __future__ import division

from decimal import getcontext

from quant.const import ORDER_TYPE, SIDE
from quant.environment import Environment
from quant.modle.order import Order

__all__ = []
getcontext().prec = 8


def export_as_api(func):
    __all__.append(func.__name__)
    return func


def _collect_signal(sinal):
    env = Environment.get_instance()
    # 信号统计
    if sinal == SIDE.BUY:
        env.buy_signal += 1
    elif sinal == SIDE.SELL:
        env.sell_signal += 1


def _order(symbol, price=None, amount=None, order_type=None, signal=None):
    order = None
    env = Environment.get_instance()
    # 限价单
    if order_type == ORDER_TYPE.LIMIT and price is not None and amount is not None:
        # limit order
        if amount == 0 or price == 0:
            return None
        side = SIDE.BUY if amount > 0 else SIDE.SELL
        order = Order.create_order(symbol, price, abs(amount), side, order_type)
    # 市价单
    elif order_type == ORDER_TYPE.MARKET:
        # market order
        last_price = env.get_last_price(symbol)
        if price is not None and price > 0:
            side = SIDE.BUY
            order = Order.create_order(symbol, last_price, price / last_price, side, order_type)
        elif amount is not None and amount < 0:
            side = SIDE.SELL
            order = Order.create_order(symbol, last_price, abs(amount), side, order_type)
    _collect_signal(sinal=signal)
    # 审核order
    if order is not None and env.can_submit_order(order):
        env.broker.submit_order(order)


@export_as_api
def buy(symbol=None, when=True):
    if when:
        all_in(symbol)


@export_as_api
def sell(symbol=None, when=True):
    if when:
        all_out(symbol)


@export_as_api
def all_in(symbol=None):
    """全仓买入"""
    env = Environment.get_instance()
    symbol = symbol or env.config.base.symbol
    account = env.get_account_by_symbol(symbol)
    return market_buy(symbol, price=account.cash)


@export_as_api
def all_out(symbol=None):
    """全仓卖出"""
    env = Environment.get_instance()
    symbol = symbol or env.config.base.symbol
    account = env.get_account_by_symbol(symbol)
    position = account.positions[symbol]
    return market_sell(symbol, amount=-abs(position.amount))


@export_as_api
def market_buy(symbol, price):
    return _order(symbol, price=price, order_type=ORDER_TYPE.MARKET, signal=SIDE.BUY)


@export_as_api
def market_sell(symbol, amount):
    return _order(symbol, amount=-abs(amount), order_type=ORDER_TYPE.MARKET, signal=SIDE.SELL)


@export_as_api
def limit_order(symbol, price, amount):
    """
    amount > 0 for buy
    amount <0 for sell
    """
    return _order(symbol, price=price, amount=amount, order_type=ORDER_TYPE.LIMIT,
                  signal=SIDE.BUY if amount > 0 else SIDE.SELL)
