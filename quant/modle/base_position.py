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
        self._cache = {}

    def __getitem__(self, key):
        if key not in self._cache:
            self._cache[key] = self._position_cls(key)
        return self._cache[key]

    def __delitem__(self, key):
        del self._cache[key]

    def __contains__(self, key):
        return key in self._cache

    def __len__(self):
        return len(self._cache)

    def values(self):
        return self._cache.values()

    def items(self):
        return self._cache.items()


class BasePosition(object):
    """仓位"""
    NaN = float('NaN')

    def __init__(self, symbol):
        self.symbol = symbol
        self._last_price = self.NaN

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
        return (self._last_price if self._last_price == self._last_price else
                Environment.get_instance().get_last_price(self.symbol))

    def apply_trade(self, trade):
        raise NotImplementedError

    __repr__ = repr_print.repr_dict
