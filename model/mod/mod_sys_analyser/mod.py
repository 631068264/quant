#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/28 14:42
@annotation = ''
"""
from model.bar import BarDict
from model.broker.back_test_broker import BackTestBroker
from model.const import RUN_TYPE
from model.data_source.base_source import BaseDataSource
from model.data_source.data_proxy import DataProxy
from model.event_source.back_test_event_source import BackTestEventSource
from model.interface import AbstractMod


class AnalyserMod(AbstractMod):
    def __init__(self):
        pass

    def stop(self, *args, **kwargs):
        pass

    def start(self, env, mod_config):
        base_config = env.config.base
        # 数据来源
        if base_config.run_type == RUN_TYPE.BACKTEST:
            env.event_source = BackTestEventSource(env)
            env.data_source = BaseDataSource()
        env.data_proxy = DataProxy(env.data_source)
        env.bar_dict = BarDict(env.data_proxy, base_config.frequency)

        # 交易处理
        if mod_config.signal:
            pass
            # TODO:SignalBroker
        else:
            env.broker = BackTestBroker(env)
        env.portfolio = env.broker.get_portfolio()
        # TODO:清理util
