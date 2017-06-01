#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 09:19
@annotation = ''
"""
from model.environment import Environment


class BasePosition(object):
    """仓位"""

    def __init__(self, symbol):
        self.symbol = symbol

    def get_state(self):
        raise NotImplementedError

    def set_state(self, state):
        raise NotImplementedError

    @property
    def market_value(self):
        """
        [float] 当前仓位市值
        """
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def last_price(self):
        """最新价"""
        return Environment.get_instance().get_last_price(self.symbol)

    def apply_trade(self, trade):
        raise NotImplementedError
