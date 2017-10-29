#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 22:31
@annotation = ''
"""
from quant import AbstractMod, RUN_TYPE, BaseDataSource, DataProxy, BarDict
from .backtest_broker import BackTestBroker
from .backtest_event_source import BackTestEventSource


class BackTestMod(AbstractMod):
    def start(self, env, mod_config):
        base_config = env.config.base
        if base_config.run_type == RUN_TYPE.BACKTEST:
            env.broker = BackTestBroker(env, mod_config)
            env.event_source = BackTestEventSource(env)

        env.portfolio = env.broker.get_portfolio()
        env.data_source = BaseDataSource()
        env.data_proxy = DataProxy(env.data_source)
        env.bar_dict = BarDict(env.data_proxy, base_config.frequency)

    def stop(self, *args, **kwargs):
        pass
