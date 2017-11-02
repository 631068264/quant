#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/19 11:02
@annotation = ''
"""
import pandas as pd
import six

from quant.data_source.bar_store import INSTRUMENT_DICT
from quant.modle.bar import Bar

valid_fields = {"open", "high", "low", "close", "volume", "datetime"}


class DataProxy(object):
    def __init__(self, data_source):
        self._data_source = data_source
        self._instruments = INSTRUMENT_DICT
        self._dates = {}

    def get_bar(self, symbol, dt, frequency):
        instrument = self.instrument(symbol)
        bar = self._data_source.get_bar(instrument, dt, frequency)
        if bar is not None:
            return Bar(instrument, bar)

    def _handle_fields(self, fields):
        if fields is None:
            return list(valid_fields)
        if isinstance(fields, six.string_types):
            return fields
        return fields

    def _valid_fields(self, fields):
        if fields is None:
            return True
        if isinstance(fields, six.string_types):
            return fields in valid_fields
        return set(fields) <= valid_fields

    def history(self, symbol, frequency, bar_count, dt, field):
        instrument = self.instrument(symbol)
        if not self._valid_fields(field):
            return None
        field = self._handle_fields(field)
        data = self._data_source.history_bar(instrument, frequency, bar_count, dt, field)
        if data is None:
            return None
        return data

    def instrument(self, symbols):
        def get_instrument(symbol):
            return self._instruments.get(symbol, None)

        if isinstance(symbols, six.string_types):
            return get_instrument(symbols)
        keys = self._instruments.keys()
        return [get_instrument(s) for s in symbols if s in keys]

    def all_instrument(self):
        return self._instruments

    def _get_calendar(self, symbol, frequency):
        return self._data_source.get_calendar(self.instrument(symbol), frequency)

    def get_calendar(self, symbol, frequency, start_date, end_date):
        trade_date = self._get_calendar(symbol, frequency)
        if trade_date is None:
            return None
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        left = trade_date.searchsorted(start_date)
        right = trade_date.searchsorted(end_date, side='right')
        if right == 0:
            return None

        return trade_date[left:right]

    def get_previous_date(self, symbol, frequency, dt, n=1):
        trade_date = self._get_calendar(symbol, frequency)
        if trade_date is None:
            return None
        dt = pd.Timestamp(dt)
        pos = trade_date.searchsorted(dt)
        if pos >= n:
            return trade_date[pos - n]
        return trade_date[0]

    def get_next_date(self, symbol, frequency, dt, n=1):
        trade_date = self._get_calendar(symbol, frequency)
        if trade_date is None:
            return None
        dt = pd.Timestamp(dt)
        pos = trade_date.searchsorted(dt, side='right')
        if pos + n > len(trade_date):
            return trade_date[-1]
        return trade_date[pos + n - 1]

    def get_calendar_range(self, symbol, frequency):
        return self._data_source.get_calendar_range(self.instrument(symbol), frequency)
