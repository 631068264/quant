#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/17 16:53
@annotation = ''
"""
from model.const import ACCOUNT_TYPE
from model.environment import Environment


class RunInfo(object):
    """
    策略运行信息
    """

    def __init__(self, config):
        base_config = config.base
        self.start_date = base_config.start_date
        self.end_date = base_config.end_date
        self.frequency = base_config.frequency
        self.spot_starting_cash = base_config.spot_starting_cash
        self.benchmark = base_config.benchmark
        self.run_type = base_config.run_type


class Context(object):
    def __init__(self):
        self._config = None

    @property
    def now(self):
        """
        使用以上的方式就可以在handle_bar中拿到当前的bar的时间，比如day bar的话就是那天的时间，minute bar的话就是这一分钟的时间点。
        """
        return Environment.get_instance().now

    @property
    def run_info(self):
        """
        :property getter: :class:`~RunInfo`
        """
        config = Environment.get_instance().config
        return RunInfo(config)

    @property
    def portfolio(self):
        """
        投资组合

        =========================   =========================   ==============================================================================
        属性                         类型                        注释
        =========================   =========================   ==============================================================================
        accounts                    dict                        账户字典
        start_date                  datetime.datetime           策略投资组合的回测/实时模拟交易的开始日期
        units                       float                       份额
        unit_net_value              float                       净值
        daily_pnl                   float                       当日盈亏，当日盈亏的加总
        daily_returns               float                       投资组合每日收益率
        total_returns               float                       投资组合总收益率
        annualized_returns          float                       投资组合的年化收益率
        total_value                 float                       投资组合总权益
        positions                   dict                        一个包含所有仓位的字典，以order_book_id作为键，position对象作为值
        cash                        float                       总的可用资金
        market_value                float                       投资组合当前的市场价值，为子组合市场价值的加总
        =========================   =========================   ==============================================================================

        :property getter: :class:`~Portfolio`
        """
        return Environment.get_instance().portfolio

    @property
    def stock_account(self):
        return self.portfolio.accounts[ACCOUNT_TYPE.SPOT]

    @property
    def config(self):
        return Environment.get_instance().config

    @property
    def symbol(self):
        return Environment.get_instance().config.base.symbol
