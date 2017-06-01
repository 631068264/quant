#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/22 10:51
@annotation = ''
"""
from __future__ import division

from model.const import ORDER_TYPE, SIDE
from model.environment import Environment
from model.order import Order

__all__ = [
    "ORDER_TYPE",
    "SIDE",
]


def export_as_api(func):
    __all__.append(func.__name__)
    return func


def _safe_market_order(order):
    """只过滤 market order"""
    if order is None:
        return None
    env = Environment.get_instance()
    account = env.get_account(order.symbol)
    if order.type == ORDER_TYPE.MARKET:
        if order.side == SIDE.BUY:
            if account.cash < order.trade_cost:
                order.reject("Not enough money [buy] {symbol} [need] {price} [cash] {cash}".format(
                    symbol=order.symbol, price=order.price * order.amount, cash=account.cash))
                return None
        elif order.side == SIDE.SELL:
            if account.positions[order.symbol] < order.amount:
                order.reject("Not enough positions [sell] {symbol} [need] {amount} [sellable] {positions}".format(
                    symbol=order.symbol, amount=order.amount, positions=account.positions[order.symbol]
                ))
                return None

    env.broker.submit_order(order)
    return order


def _order(symbol, price=None, amount=None, order_type=None):
    order = None
    if order_type == ORDER_TYPE.LIMIT and price is not None and amount is not None:
        # limit order
        if amount == 0 or price == 0:
            # TODO:log
            return None
        side = SIDE.BUY if amount > 0 else SIDE.SELL
        order = Order.create_order(symbol, price, abs(amount), side, order_type)
    elif order_type == ORDER_TYPE.MARKET:
        # market order
        last_price = Environment.get_instance().get_last_price(symbol)
        if price is not None and price > 0:
            side = SIDE.BUY
            amount = float(price / last_price)
            order = Order.create_order(symbol, price, amount, side, order_type)
        elif amount is not None and amount < 0:
            side = SIDE.SELL
            last_price = Environment.get_instance().get_last_price(symbol)
            order = Order.create_order(symbol, last_price, abs(amount), side, order_type)

    return _safe_market_order(order)


def all_in(symbol):
    env = Environment.get_instance()
    account = env.get_account(symbol)
    return market_buy(symbol, price=account.cash)


def all_out(symbol):
    env = Environment.get_instance()
    account = env.get_account(symbol)
    position = account.positions[symbol]
    return market_sell(symbol, amount=position.amount)


def market_buy(symbol, price):
    return _order(symbol, price=price, order_type=ORDER_TYPE.MARKET)


def market_sell(symbol, amount):
    return _order(symbol, amount=amount, order_type=ORDER_TYPE.MARKET)


def limit_order(symbol, price, amount):
    """
    amount <0 for buy
    amount > 0 for sell
    """
    return _order(symbol, price=price, amount=amount, order_type=ORDER_TYPE.LIMIT)
