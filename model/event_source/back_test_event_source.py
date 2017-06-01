#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/24 14:59
@annotation = ''
"""
from model.events import Event, EVENT
from model.interface import AbstractEventSource


class BackTestEventSource(AbstractEventSource):
    def __init__(self, env):
        self._env = env

    def events(self, start_date, end_date, frequency):
        for dt in self._env.get_calendar(frequency, start_date, end_date):
            dt = dt.to_pydatetime()
            yield Event(EVENT.BEFORE_TRADING, calendar_dt=dt, trading_dt=dt)
            yield Event(EVENT.BAR, calendar_dt=dt, trading_dt=dt)
            yield Event(EVENT.AFTER_TRADING, calendar_dt=dt, trading_dt=dt)
            yield Event(EVENT.SETTLEMENT, calendar_dt=dt, trading_dt=dt)
