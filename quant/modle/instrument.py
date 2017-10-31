#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 11:43
@annotation = ''
"""

from quant.const import ACCOUNT_TYPE
from quant.util import repr_print


class Instrument(object):
    def __init__(self, exchange, pair, fee, min_amount):
        """
        金融商品
        :param exchange: 交易所
        :param pair: 交易货币对
        :param fee: 费率 和点差有区别
        :param min_amount: 最小交易量
        """
        self.exchange = exchange.lower()
        self.pair = pair.lower()
        self.fee = fee * 0.01
        self.min_amount = min_amount
        self.symbol = "%s_%s" % (self.exchange, self.pair)
        self.table_format = self.symbol + "_%s"

    def bar_name(self, frequency):
        return self.table_format % frequency

    @property
    def type(self):
        """判断symbol 期货 现货"""
        if "future" in self.symbol:
            return ACCOUNT_TYPE.FUTURE.name
        return ACCOUNT_TYPE.CRYPTO.name

    __repr__ = repr_print.repr_dict
