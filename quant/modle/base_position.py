#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 09:19
@annotation = ''
"""
from quant.environment import Environment
from quant.util import repr_print


class Positions(dict):
    def __init__(self, position_cls):
        super(Positions, self).__init__()
        self._position_cls = position_cls
        self._cached_positions = {}

    def __missing__(self, key):
        if key not in self._cached_positions:
            self._cached_positions[key] = self._position_cls(key)
        return self._cached_positions[key]

    def get_or_create(self, key):
        if key not in self:
            self[key] = self._position_cls(key)
        return self[key]


class BasePosition(object):
    """仓位"""

    def __init__(self, symbol):
        self.symbol = symbol

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

    __repr__ = repr_print.repr_dict
