#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/18 10:14
@annotation = ''
"""
from quant.data_source import get_all_bar, get_trade_date
from quant.interface import AbstractDataSource


class BaseDataSource(AbstractDataSource):
    def get_bar(self, instrument, dt, frequency):
        try:
            bars = get_all_bar(instrument, frequency)
            pos = bars['datetime'].searchsorted(dt)
            if pos >= len(bars) or bars['datetime'][pos].to_pydatetime() != dt:
                return None
            return bars[pos]
        except Exception as e:
            return None

    def get_calendar_range(self, instrument, frequency):
        try:
            date_bar = get_trade_date(instrument, frequency)
            return date_bar[0], date_bar[-1]
        except Exception as e:
            raise e

    def history_bar(self, instrument, frequency, bar_count, dt, fields):
        try:
            bars = get_all_bar(instrument, frequency)
            if bars is None:
                return None
            right = bars['datetime'].searchsorted(dt, side='right')
            left = right - bar_count if right >= bar_count else 0
            bars = bars[left:right]
            return bars if fields is None else bars[fields]
        except Exception as e:
            return None

    def get_calendar(self, instrument, frequency):
        try:
            date_bar = get_trade_date(instrument, frequency)
            return date_bar
        except Exception as e:
            return None
