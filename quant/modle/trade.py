#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 14:55
@annotation = ''
"""
import time

from quant import id_gen, safe_float
from quant.const import SIDE
from quant.environment import Environment
from quant.exception import ApplyException


class Trade(object):
    """订单"""

    def __init__(self):
        self.order_id = None
        self.create_dt = None
        self.trade_dt = None
        self.price = None
        self.amount = None
        self.trade_cost = None
        self.fee = None  # 手续费
        self.trade_id = None
        self.symbol = None
        self.side = None
        self.price = None

    @classmethod
    def create_trade(cls, order_id, symbol, side, frozen_price=float(0),
                     frozen_amount=float(0), fee=0., trade_cost=float(0)):
        env = Environment.get_instance()
        trade = cls()
        trade.order_id = order_id
        trade.symbol = symbol
        trade.side = side
        trade.create_dt = env.calendar_dt
        trade.trade_dt = env.trading_dt
        trade.fee = fee
        trade.price = frozen_price
        trade.amount = frozen_amount
        trade.trade_cost = trade_cost
        trade.trade_id = next(id_gen(int(time.time())))
        return trade

    @property
    def amount_after_fee(self):
        """交易后 所得要扣手续费"""
        if self.side != SIDE.BUY:
            raise ApplyException("just for SIDE.BUY")
        return safe_float(self.amount * (1 - self.fee))

    @property
    def price_after_fee(self):
        """交易后 所得要扣手续费"""
        if self.side != SIDE.SELL:
            raise ApplyException("just for SIDE.SELL")
        return safe_float(self.price * (1 - self.fee))
