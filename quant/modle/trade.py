#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 14:55
@annotation = ''
"""
import time

from quant import id_gen
from quant.environment import Environment


class Trade(object):
    """订单"""

    def __init__(self):
        self.trade_id = None
        self.order_id = None
        self.create_dt = None
        self.trade_dt = None
        self.symbol = None
        self.side = None
        self.fee = None
        self.price = None
        self.frozen_price = None
        self.amount = None

    @classmethod
    def create_trade(cls, order_id, symbol, side, price=0., frozen_price=0.,
                     amount=0., fee=0.):
        env = Environment.get_instance()
        trade = cls()
        trade.trade_id = next(id_gen(int(time.time())))
        trade.order_id = order_id
        trade.create_dt = env.calendar_dt
        trade.trade_dt = env.trading_dt
        trade.symbol = symbol
        trade.side = side
        trade.fee = fee
        trade.price = price
        trade.frozen_price = frozen_price
        trade.amount = amount
        return trade
