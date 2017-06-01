#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 14:55
@annotation = ''
"""
import time

from model import id_gen
from model.const import ORDER_STATUS, ORDER_TYPE, SIDE
from model.environment import Environment


class Order(object):
    """订单"""

    def __init__(self):
        self.order_id = None
        self.create_dt = None
        self.trade_dt = None
        # frozen for account sell
        self.amount = None
        # frozen for account buy
        self.trade_cost = None
        self.price = None
        self.symbol = None
        self.side = None
        self.status = None
        self.type = None
        self.message = None

    @classmethod
    def create_order(cls, symbol, price=float(0),
                     amount=float(0), side=None, style=None):
        env = Environment.get_instance()
        instrument = Environment.get_instance().get_instrument(symbol)
        order = cls()
        order.order_id = next(id_gen(int(time.time())))
        order.create_dt = env.create_dt
        order.trade_dt = env.trade_dt
        order.amount = float(amount)
        if order.amount < instrument.min_amount:
            return None
        order.price = float(price)
        order.symbol = symbol
        order.side = side
        order.message = ""
        order.status = ORDER_STATUS.PENDING_NEW
        order.type = style
        order.avg_price = 0
        order.trade_cost = cls._cal_trade_cost(price, amount, side, style)
        return order

    @classmethod
    def _cal_trade_cost(cls, price=float(0), amount=float(0), side=None, style=None):
        """"""
        if side == SIDE.SELL:
            return float(0)
        if style == ORDER_TYPE.LIMIT:
            trade_cost = price * amount
        else:
            trade_cost = price
        return float(trade_cost)

    def is_final(self):
        return self.status not in {
            ORDER_STATUS.PENDING_NEW,
            ORDER_STATUS.ACTIVE,
            ORDER_STATUS.PENDING_CANCEL
        }

    def active(self):
        self.status = ORDER_STATUS.ACTIVE

    def fill(self):
        self.status = ORDER_STATUS.FILLED

    def reject(self, reject_reason):
        # TODO:log
        if not self.is_final():
            self.message = reject_reason
            self.status = ORDER_STATUS.REJECTED

    def cancel(self, cancelled_reason):
        if not self.is_final():
            self.message = cancelled_reason
            self.status = ORDER_STATUS.CANCELLED
