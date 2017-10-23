#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/20 11:19
@annotation = ''
"""
from api import export_as_api
from quant import AbstractMod
from quant.const import ACCOUNT_TYPE
from .account import StockAccount, BenchmarkAccount
from .api import api_stock
from .position import StockPosition


class AccountMod(AbstractMod):
    def stop(self, *args, **kwargs):
        pass

    def start(self, env, mod_config):
        env.set_account(ACCOUNT_TYPE.STOCK.name, StockAccount)
        env.set_account(ACCOUNT_TYPE.BENCHMARK.name, BenchmarkAccount)

        env.set_positon(ACCOUNT_TYPE.STOCK.name, StockPosition)

        if ACCOUNT_TYPE.STOCK.name in env.config.base.accounts:
            # 注入股票API
            for export_name in api_stock.__all__:
                export_as_api(getattr(api_stock, export_name))
