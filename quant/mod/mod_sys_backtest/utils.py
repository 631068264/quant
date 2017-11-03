#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/24 14:25
@annotation = ''
"""
import six

from quant.const import ACCOUNT_TYPE
from quant.modle.base_position import Positions
from quant.modle.portfolio import Portfolio
from quant.util.exception import CashTooLessException


def init_portfolio(env):
    accounts = {}
    base_config = env.config.base
    start_date = base_config.start_date
    total_cash = 0

    try:
        for account_type, starting_cash in base_config.accounts.items():
            if starting_cash <= 0:
                raise CashTooLessException("[starting_cash]%s <= 0" % starting_cash)
            if account_type not in ACCOUNT_TYPE.__members__.keys():
                raise RuntimeError('Not allow ACCOUNT_TYPE %s' % (account_type,))

            account_model = env.get_account(account_type)
            position_model = env.get_position(account_type)
            account = account_model(starting_cash, Positions(position_model))
            total_cash += account.total_value
            accounts[account_type] = account

        return Portfolio(start_date, total_cash, accounts)
    except Exception as e:
        raise e


def create_benchmark_portfolio(env):
    # TODO:benchmark 适配
    base_config = env.config.base

    # adjust benchmark
    symbol = getattr(base_config, "symbol", None)
    benchmark = getattr(base_config, "benchmark", None)
    if isinstance(symbol, six.string_types) and benchmark is None:
        base_config.benchmark = symbol

    BenchmarkAccount = env.get_account(ACCOUNT_TYPE.BENCHMARK.name)
    BenchmarkPosition = env.get_position(ACCOUNT_TYPE.BENCHMARK.name)
    total_cash = sum(base_config.accounts.values())
    accounts = {
        ACCOUNT_TYPE.BENCHMARK.name: BenchmarkAccount(total_cash, Positions(BenchmarkPosition)),
    }
    return Portfolio(base_config.start_date, total_cash, accounts)
