#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 11:43
@annotation = ''
"""

import six

from model import repr_dict
from model.const import ACCOUNT_TYPE


class Instrument(object):
    def __init__(self, exchange, pair, fee, min_amount, table_format):
        # 交易所
        self._exchange = exchange
        # 交易货币对
        self._pair = pair
        self._fee = fee
        # 最小交易量
        self._min_amount = min_amount
        self._table_format = table_format
        assert (0 < self._fee < 1), self.symbol

    @property
    def symbol(self):
        return "%s_%s" % (self._exchange.lower(), self._pair.lower())

    @property
    def exchange(self):
        return self._exchange.lower()

    @property
    def fee(self):
        return self._fee * 0.01

    @property
    def min_amount(self):
        return self._min_amount

    def bar_name(self, frequency):
        return self._table_format % frequency

    @property
    def type(self):
        """判断symbol 期货 现货"""
        if "future" in self.symbol:
            return ACCOUNT_TYPE.FUTURE
        return ACCOUNT_TYPE.SPOT

    __repr__ = repr_dict


def get_all_instrument(instrument_info=None):
    instruments = {}

    for exchange, infos in six.iteritems(instrument_info):
        for info in infos:
            instrument = Instrument(exchange, **info)
            instruments[instrument.symbol] = instrument
    return instruments
