#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 21:11
@annotation = ''
"""
from .benchmark_account import BenchmarkAccount
from .stock_account import StockAccount


def create_benchmark_portfolio(env):
    from quant.const import ACCOUNT_TYPE
    from quant.mod.mod_sys_account.position import Positions, SpotPosition
    from quant.modle.portfolio import Portfolio
    accounts = {}
    base_config = env.config.base
    total_cash = 0
    for account_type in base_config.account:
        if account_type == ACCOUNT_TYPE.STOCK:
            total_cash += base_config.spot_starting_cash
        elif account_type == ACCOUNT_TYPE.FUTURE:
            total_cash += base_config.future_starting_cash
        else:
            raise NotImplementedError
    accounts[ACCOUNT_TYPE.BENCHMARK] = BenchmarkAccount(total_cash, Positions(SpotPosition))

    return Portfolio(base_config.start_date, total_cash, accounts)
