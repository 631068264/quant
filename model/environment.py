#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/17 16:38
@annotation = ''
"""
import datetime
from collections import defaultdict

from model import AttrDict
from model.const import FREQUENCY, ACCOUNT_TYPE, RUN_TYPE
from model.events import EventBus


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Environment(object):
    _env = None

    def __init__(self, config):
        Environment._env = self
        self.config = parse_config(config)
        self.data_proxy = None
        self.data_source = None
        self.event_source = None
        self.broker = None
        self.profile_deco = None
        # self.system_log = system_log
        # self.user_log = user_log
        # self.user_detail_log = user_detail_log
        self.event_bus = EventBus()
        self.portfolio = None
        self.benchmark_portfolio = None
        self.calendar_dt = self.config.base.start_date
        self.trading_dt = self.config.base.start_date
        self.plot_store = None
        self.bar_dict = None

    @classmethod
    def get_instance(cls):
        return Environment._env

    def get_bar(self, symbol):
        return self.bar_dict[symbol]

    def get_last_price(self, symbol):
        return self.bar_dict[symbol].last

    def get_instrument(self, symbol):
        return self.data_proxy.instrument(symbol)

    def get_account(self, symbol):
        account_type = self.get_instrument(symbol).type
        return self.portfolio.accounts[account_type]

    def history(self, symbol, frequency, bar_count, dt, fields):
        if frequency is None:
            frequency = self.config.base.frequency
        if frequency not in FREQUENCY.ALL:
            return None
        return self.data_proxy.history(symbol, frequency, bar_count, dt, fields)

    # def get_trade_date(self, symbol, frequency, start_date, end_date):
    #     return self.data_proxy.get_trade_date(symbol, frequency, start_date, end_date)

    def get_previous_date(self, symbol, frequency, dt, n=1):
        return self.data_proxy.get_previous_date(symbol, frequency, dt, n=n)

    def get_next_date(self, symbol, frequency, dt):
        return self.data_proxy.get_next_date(symbol, frequency, dt)

    def get_calendar(self, frequency, start_date, end_date):
        return self.data_proxy.get_calendar("okcn_btc_cny", frequency, start_date, end_date)

    def get_calendar_range(self, frequency):
        return self.data_proxy.get_calendar_range("okcn_btc_cny", frequency)

    def get_plot_store(self):
        if self.plot_store is None:
            self.plot_store = PlotStore()
        return self.plot_store

    def add_plot(self, series_name, value):
        self.get_plot_store().add_plot(self.trading_dt, series_name, value)


class PlotStore(object):
    def __init__(self):
        self._plots = defaultdict(dict)

    def add_plot(self, dt, series_name, value):
        self._plots[series_name][dt] = value

    def get_plots(self):
        return self._plots


def parse_config(config):
    def parse_date(config_date):
        dt = datetime.datetime.strptime(config_date, "%Y-%m-%d")
        return dt.replace(microsecond=0)

    config = AttrDict(config)
    base_config = config.base

    base_config.start_date = parse_date(base_config.start_date)
    base_config.end_date = parse_date(base_config.end_date)
    assert base_config.start_date < base_config.end_date
    assert base_config.frequency in FREQUENCY.ALL
    assert set(base_config.account) <= set(ACCOUNT_TYPE.__members__.values())
    assert base_config.run_type in RUN_TYPE.__members__.values()

    config.base = base_config

    return config
