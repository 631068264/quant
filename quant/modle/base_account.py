#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 17:21
@annotation = ''
"""
import six

from quant.util import repr_print


# TODO:不同account——type benchmark 的symbol不一样
class BaseAccount(object):
    def __init__(self, total_cash, positions, register_event=True):
        self.positions = positions
        self.frozen_cash = 0
        self.total_cash = total_cash

        if register_event:
            self.register_event()

    def register_event(self):
        """
        注册事件
        """
        raise NotImplementedError

    @property
    def type(self):
        """
        [enum] 账户类型
        """
        raise NotImplementedError

    @property
    def total_value(self):
        """
        [float] 净资产
        """
        raise NotImplementedError

    @property
    def cash(self):
        """
        [float] 可用资金
        """
        return self.total_cash - self.frozen_cash

    @property
    def total_market_value(self):
        """
        [float] 总市值
        """
        return sum(position.market_value for position in six.itervalues(self.positions))

    @property
    def market_value(self):
        """
        [dict] 不同货币对应的市值
        :return:
        """
        return {position.symbol: position.market_value for position in six.itervalues(self.positions)}

    @property
    def frozen_amount(self):
        return {position.symbol: position.frozen_amount for position in six.itervalues(self.positions)}

    __repr__ = repr_print.repr_dict
