#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 14:55
@annotation = ''
"""
import time

from quant.const import ORDER_STATUS
from quant.environment import Environment
from quant.util import id_gen
from quant.util import repr_print


class Order(object):
    """订单"""
    __repr__ = repr_print.repr_dict

    def __init__(self):
        self.order_id = None
        self.create_dt = None
        self.trade_dt = None
        self.symbol = None
        self.price = None
        self.amount = None
        self.fill_amount = None
        self.fee = None
        self.side = None
        self.type = None
        self.status = None
        self.message = None

    @classmethod
    def create_order(cls, symbol, price=0.,
                     amount=0., side=None, style=None):
        env = Environment.get_instance()
        symbol = symbol or env.config.base.symbol
        instrument = env.get_instrument(symbol)
        order = cls()
        order.order_id = next(env.id)
        order.create_dt = env.calendar_dt
        order.trade_dt = env.trading_dt
        order.symbol = symbol
        order.price = price
        order.amount = amount
        if order.amount < instrument.min_amount:
            raise ValueError('order amount should > min_amount')
        order.fill_amount = 0.
        order.fee = instrument.fee
        order.side = side
        order.type = style
        order.status = ORDER_STATUS.PENDING_NEW
        order.message = ""
        return order

    def is_final(self):
        return self.status not in {
            ORDER_STATUS.PENDING_NEW,
            ORDER_STATUS.ACTIVE,
            ORDER_STATUS.PENDING_CANCEL
        }

    def active(self):
        self.status = ORDER_STATUS.ACTIVE

    @property
    def unfilled_amount(self):
        return self.amount - self.fill_amount

    def fill(self, trade):
        amount = self.fill_amount + trade.amount
        assert amount <= self.amount
        self.fill_amount = amount
        if self.unfilled_amount == 0:
            self.status = ORDER_STATUS.FILLED

    def reject(self, reject_reason):
        if not self.is_final():
            self.message = reject_reason
            self.status = ORDER_STATUS.REJECTED

    def cancel(self, cancelled_reason):
        if not self.is_final():
            self.message = cancelled_reason
            self.status = ORDER_STATUS.CANCELLED
