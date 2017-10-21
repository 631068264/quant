#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 11:43
@annotation = ''
"""

from model import repr_dict
from model.const import ACCOUNT_TYPE


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

    def bar_name(self, period):
        return self.table_format % period

    @property
    def type(self):
        """判断symbol 期货 现货"""
        if "future" in self.symbol:
            return ACCOUNT_TYPE.FUTURE.name
        return ACCOUNT_TYPE.STOCK.name

    __repr__ = repr_dict


def get_all_instrument(instrument_info):
    instruments = {}
    for exchange, infos in instrument_info.items():
        for info in infos:
            instrument = Instrument(exchange, **info)
            instruments[instrument.symbol] = instrument
    return instruments
