#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 11:24
@annotation = ''
"""

import numpy as np

from quant.util import repr_print
from quant.util.datetime_func import convert_to_datetime

OHLCV = ['open', 'high', 'low', 'close', 'volume']
NANDict = {i: np.nan for i in OHLCV}


class Bar(object):
    """
    K线 candle
    """

    # TODO: 是否可交易 if volume > 0
    def __init__(self, instrument, data=None, dt=None):
        self._instrument = instrument
        # TODO:获取 depth
        self._data = data if data is not None else NANDict
        self._dt = dt

    @property
    def open(self):
        """
        [float] 当日开盘价
        """
        return self._data["open"]

    @property
    def high(self):
        """
        [float] 截止到当前的最高价
        """
        return self._data["high"]

    @property
    def low(self):
        """
        [float] 截止到当前的最低价
        """
        return self._data["low"]

    @property
    def close(self):
        return self._data["close"]

    @property
    def last(self):
        """
        [float] 当前最新价
        """
        return self.close

    @property
    def volume(self):
        """
        [float] 截止到当前的成交量
        """
        return self._data["volume"]

    @property
    def datetime(self):
        return convert_to_datetime(self._data['datetime']) \
            if self._dt is None else self._dt

    @property
    def instrument(self):
        return self._instrument


class BarDict(object):
    def __init__(self, data_proxy, frequency):
        self._data_proxy = data_proxy
        self._frequency = frequency
        self._cache = {}
        self._dt = None

    def update_dt(self, dt):
        self._dt = dt
        self._cache.clear()

    def __getitem__(self, key):
        instrument = self._data_proxy.instrument(key)
        if instrument is None:
            raise KeyError('invalid symbol : {}'.format(key))
        symbol = instrument.symbol
        try:
            return self._cache[symbol]
        except KeyError:
            bar = self._data_proxy.get_bar(symbol, self._dt, self._frequency)
            if bar is None:
                return Bar(instrument, NANDict, self._dt)
            else:
                self._cache[symbol] = bar
                return bar

    @property
    def dt(self):
        return self._dt

    __repr__ = repr_print.repr_dict
