#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 22:31
@annotation = ''
"""
from quant.const import RUN_TYPE
from quant.data_source.base_data_source import BaseDataSource
from quant.data_source.data_proxy import DataProxy
from quant.interface import AbstractMod
from quant.modle.bar import BarDict
from .backtest.backtest_broker import BackTestBroker
from .backtest.backtest_event_source import BackTestEventSource
from .utils import create_benchmark_portfolio


class BackTestMod(AbstractMod):
    def start(self, env, mod_config):
        base_config = env.config.base
        if base_config.run_type == RUN_TYPE.BACKTEST:
            env.broker = BackTestBroker(env, mod_config)
            env.event_source = BackTestEventSource(env)
            env.data_source = BaseDataSource()
        elif base_config.run_type in (RUN_TYPE.PAPER_TRADING,RUN_TYPE.LIVE_TRADING):
            # env.data_source = RedisDataSource()
            # env.event_source = RealTimeEventSource(env)
            pass

        env.portfolio = env.broker.get_portfolio()
        env.benchmark_portfolio = create_benchmark_portfolio(env)
        env.data_proxy = DataProxy(env.data_source)
        env.bar_dict = BarDict(env.data_proxy, base_config.frequency)

    def stop(self, *args, **kwargs):
        pass
