#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 09:19
@annotation = ''
"""
from model.base_position import BasePosition
from model.const import ACCOUNT_TYPE, SIDE


class StockPosition(BasePosition):
    def __init__(self, symbol):
        super(StockPosition, self).__init__(symbol)
        self.amount = 0  # 持币数量
        self.frozen_amount = 0  # 冻结量
        self.buy_price = 0  # 买入价

    def apply_trade(self, trade):
        if trade.side == SIDE.BUY:
            self.amount += trade.amount_after_fee
            self.buy_price = trade.price
        else:
            self.amount -= trade.amount
            self.frozen_amount -= trade.amount

    def on_order_pending_new(self, order):
        if order.side == SIDE.SELL:
            self.frozen_amount += order.amount

    def on_order_cancel(self, order):
        if order.side == SIDE.SELL:
            self.frozen_amount -= order.amount

    @property
    def earning(self):
        """持仓收益"""
        return self.amount * (self.last_price - self.buy_price)

    @property
    def market_value(self):
        """市价"""
        return self.amount * self.last_price

    @property
    def type(self):
        return ACCOUNT_TYPE.STOCK.name
