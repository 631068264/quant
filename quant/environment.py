#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/17 16:38
@annotation = ''
"""

from quant.const import FREQUENCY
from quant.events import EventBus
from quant.util.config import parse_config


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
        # TODO:dt之间区别
        self.calendar_dt = self.config.base.start_date
        self.trading_dt = self.config.base.start_date
        self.plot_store = None
        self.bar_dict = None
        # model dict
        self._account_dict = {}
        self._position_dict = {}
        # validator
        self._validator = []
        # 信号统计
        self.buy_signal = 0
        self.sell_signal = 0

    @classmethod
    def get_instance(cls):
        return Environment._env

    def set_account(self, account_type, account_model):
        self._account_dict[account_type] = account_model

    def get_account(self, account_type):
        try:
            return self._account_dict[account_type]
        except Exception as e:
            raise KeyError('Unknown Account Type %s' % (account_type,))

    def set_position(self, position_type, position_model):
        self._position_dict[position_type] = position_model

    def get_position(self, position_type):
        try:
            return self._position_dict[position_type]
        except Exception as e:
            raise KeyError('Unknown Position Type %s' % (position_type,))

    def add_validator(self, validator):
        self._validator.append(validator)

    def can_submit_order(self, order):
        account = self.get_account_by_symbol(order.symbol)
        for v in self._validator:
            if not v.can_submit_order(account, order):
                return False
        return True

    def can_cancel_order(self, order):
        if order.is_final():
            return False
        account = self.get_account_by_symbol(order.symbol)
        for v in self._validator:
            if not v.can_cancel_order(account, order):
                return False
        return True

    def get_bar(self, symbol):
        return self.bar_dict[symbol]

    def get_last_price(self, symbol):
        return float(self.bar_dict[symbol].last)

    def get_instrument(self, symbol):
        return self.data_proxy.instrument(symbol)

    def get_account_by_symbol(self, symbol):
        account_type = self.get_instrument(symbol).type
        return self.portfolio.accounts[account_type]

    def history(self, symbol, frequency, bar_count, dt, fields):

        def _check_frequency():
            if frequency and frequency not in FREQUENCY.ALL:
                raise RuntimeError('{} not in data frequency'.format(frequency))
            return frequency or self.config.base.frequency

        def _check_symbol():
            return symbol or self.config.base.symbol

        frequency = _check_frequency()
        symbol = _check_symbol()
        return self.data_proxy.history(symbol, frequency, bar_count, dt, fields)

    def get_previous_date(self, symbol, frequency, dt, n=1):
        return self.data_proxy.get_previous_date(symbol, frequency, dt, n=n)

    def get_next_date(self, symbol, frequency, dt):
        return self.data_proxy.get_next_date(symbol, frequency, dt)

    def get_calendar(self, benchmark_symbol, frequency, start_date, end_date):
        return self.data_proxy.get_calendar(benchmark_symbol, frequency, start_date, end_date)

    def get_calendar_range(self, benchmark_symbol, frequency):
        return self.data_proxy.get_calendar_range(benchmark_symbol, frequency)

    def add_plot(self, series_name, value):
        self.get_plot_store().add_plot(self.trading_dt, series_name, value)

    def get_plot_store(self):
        if self.plot_store is None:
            from quant.util.plot_store import PlotStore
            self.plot_store = PlotStore()
        return self.plot_store

    def get_plot_bar(self):
        base_config = self.config.base
        symbol = base_config.symbol
        frequency = base_config.frequency
        star_dt = base_config.start_date
        end_dt = base_config.end_date
        return self.data_proxy.get_plot_bar(symbol, frequency, star_dt, end_dt)
