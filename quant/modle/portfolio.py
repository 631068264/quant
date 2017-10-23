#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 15:54
@annotation = ''
"""
from __future__ import division

import six

from quant.const import ACCOUNT_TYPE
from quant.environment import Environment
from quant.events import EVENT
from quant.exception import CashTooLessException
from quant.mod.mod_sys_account.account import SpotAccount
from quant.mod.mod_sys_account.position import Positions
from quant.mod.mod_sys_account.position import SpotPosition

DAYS_A_YEAR = 365


class Portfolio(object):
    def __init__(self, start_date, start_cash, accounts):
        # 策略投资组合的开始日期
        self.start_date = start_date
        self.accounts = accounts
        # 初始资金
        self.start_cash = start_cash
        # 交易前总权益
        self.static_total_value = 0
        self.register_event()

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        event_bus.prepend_listener(EVENT.PRE_BEFORE_TRADING, self._pre_before_trading)

    @property
    def spot_account(self):
        """
        [StockAccount] 现货账户
        """
        return self.accounts.get(ACCOUNT_TYPE.STOCK, None)

    @property
    def total_value(self):
        """
        [float] 总收益 = 可用资金 + 市值
        """
        return sum(account.total_value for account in self.accounts.values())

    @property
    def cash(self):
        """
        [float] 可用资金
        """
        return sum(account.cash for account in self.accounts.values())

    @property
    def total_market_value(self):
        """
        [float] 市值 sum(拥有的货币数量 * 对应的最新价)
        """
        return sum(account.total_market_value for account in six.itervalues(self.accounts))

    @property
    def market_value(self):
        return {account.type.name: account.market_value for account in six.itervalues(self.accounts)}

    @property
    def frozen_cash(self):
        return sum(account.frozen_cash for account in six.itervalues(self.accounts))

    @property
    def frozen_amount(self):
        return {account.type.name: account.frozen_amount for account in six.itervalues(self.accounts)}

    def _pre_before_trading(self, event):
        self.static_total_value = self.total_value

    @property
    def current_pnl(self):
        """交易后-交易前"""
        return self.total_value - self.static_total_value

    @property
    def current_pnl_returns(self):
        return 0 if self.static_total_value == 0 else self.current_pnl / self.static_total_value

    @property
    def pnl(self):
        """盈亏"""
        return self.total_value - self.start_cash

    @property
    def pnl_returns(self):
        """收益率"""
        return self.pnl / self.start_cash

    @property
    def annualized_returns(self):
        """
        [float] 年化收益率
        """
        current_date = Environment.get_instance().trading_dt.date()
        return (1 + self.pnl_returns) ** (DAYS_A_YEAR / float((current_date - self.start_date.date()).days + 1)) - 1

    @property
    def unit_net_value(self):
        return self.total_value / self.start_cash


def init_portfolio(env):
    accounts = {}
    base_config = env.config.base
    start_date = base_config.start_date
    total_cash = 0
    try:
        for account_type in base_config.account:
            if account_type == ACCOUNT_TYPE.STOCK:
                spot_starting_cash = base_config.spot_starting_cash
                if spot_starting_cash <= 0:
                    raise CashTooLessException("[spot_starting_cash]%s <= 0" % spot_starting_cash)
                total_cash += spot_starting_cash
                accounts[ACCOUNT_TYPE.STOCK] = SpotAccount(spot_starting_cash, Positions(SpotPosition))

            elif account_type == ACCOUNT_TYPE.FUTURE:
                raise NotImplementedError
            else:
                raise NotImplementedError
        return Portfolio(start_date, total_cash, accounts)

    except Exception as e:
        raise e
