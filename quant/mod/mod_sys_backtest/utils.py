#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/24 14:25
@annotation = ''
"""
from quant import ACCOUNT_TYPE, CashTooLessException, Portfolio
from quant.modle.base_position import Positions


def init_portfolio(env):
    accounts = {}
    base_config = env.config.base
    start_date = base_config.start_date
    total_cash = 0
    try:
        for account_type, starting_cash in base_config.account.items():
            if starting_cash <= 0:
                raise CashTooLessException("[starting_cash]%s <= 0" % starting_cash)
            if account_type == ACCOUNT_TYPE.CRYPTO.name:
                CryptoAccount = env.get_account(account_type)
                CryptoPosition = env.get_position(account_type)
                total_cash += starting_cash
                accounts[account_type] = CryptoAccount(starting_cash, Positions(CryptoPosition))

            elif account_type == ACCOUNT_TYPE.FUTURE.name:
                raise NotImplementedError
            else:
                raise NotImplementedError
        return Portfolio(start_date, total_cash, accounts)

    except Exception as e:
        raise e
