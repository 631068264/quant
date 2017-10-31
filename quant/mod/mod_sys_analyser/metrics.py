#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/26 17:04
@annotation = ''
"""
from __future__ import division

import numpy as np

TRADE_DAY_A_YEAR = 365


class Metrics(object):
    """回测数据度量"""

    def __init__(self, portfolio_returns, benchmark_returns, days):
        assert (len(portfolio_returns) == len(benchmark_returns))
        self._portfolio_returns = portfolio_returns
        self._benchmark_returns = benchmark_returns
        self._trade_days = days
        self._annual_factor = TRADE_DAY_A_YEAR

        # TODO:干掉重复计算
        self.alpha, self.beta = self._cal_alpha_beta()
        self.sharpe = self._cal_sharpe()
        self.max_drawdown = self._max_drawdown()
        self.volatility = self._cal_volatility()
        self.information_ratio = self._cal_information()
        self.downside_risk = self._cal_downside_risk()
        self.sortino = self._cal_sortino()
        self.tracking_error = self._cal_tracking_error()

    def _cal_max_drawdown(self):
        """最大回撤"""
        if len(self._portfolio_returns) < 1:
            self._max_drawdown = np.nan
            return 0

        df_cum = np.exp(np.log1p(self._portfolio_returns).cumsum())
        max_return = np.maximum.accumulate(df_cum)
        return abs(((df_cum - max_return) / max_return).min())

    def _cal_volatility(self):
        """波动率"""
        if len(self._portfolio_returns) < 2:
            return 0
        volatility = np.std(self._portfolio_returns, ddof=1)
        return np.sqrt(self._annual_factor) * volatility

    def _cal_sharpe(self):
        """夏普率"""
        if len(self._portfolio_returns) < 2:
            return 0
        std_returns = np.std(self._portfolio_returns, ddof=1)
        if std_returns == 0:
            return 0
        return np.sqrt(self._annual_factor) * np.mean(self._portfolio_returns) / std_returns

    def _cal_tracking_error(self):
        """年化跟踪误差"""
        active_return = self._portfolio_returns - self._benchmark_returns
        tracking_error = np.std(active_return, ddof=1)
        return np.sqrt(self._annual_factor) * tracking_error

    def _cal_information(self):
        """信息比率"""
        if len(self._portfolio_returns) < 2:
            return 0
        active_return = self._portfolio_returns - self._benchmark_returns
        tracking_error = np.std(active_return, ddof=1)
        if tracking_error == 0:
            return 0
        return np.sqrt(self._annual_factor) * np.mean(active_return) / tracking_error

    def _cal_alpha_beta(self):
        if len(self._portfolio_returns) < 2 or len(self._benchmark_returns) < 2:
            return 0, 0
        cov = np.cov(np.vstack([
            self._portfolio_returns,
            self._benchmark_returns
        ]), ddof=1)
        beta = cov[0, 1] / cov[1, 1]
        alpha = self._annual_factor * np.mean(self._portfolio_returns - beta * self._benchmark_returns)
        return alpha, beta

    def _cal_downside_risk(self):
        """年化下行波动率"""
        if len(self._portfolio_returns) < 2:
            return 0
        diff = self._portfolio_returns - self._benchmark_returns
        diff[diff > 0] = 0.
        return np.sqrt(np.mean(np.square(diff))) * np.sqrt(self._annual_factor)

    def _cal_sortino(self):
        """索提诺比率"""
        downside_risk = self._cal_downside_risk()
        if downside_risk == 0:
            return 0

        return self._annual_factor * np.mean(self._portfolio_returns) / downside_risk

    @property
    def all(self):
        """所有度量"""
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'sharpe': self.sharpe,
            'max_drawdown': self.max_drawdown,
            'volatility': self.volatility,
            'information_ratio': self.information_ratio,
            'downside_risk': self.downside_risk,
            'sortino': self.sortino,
            'tracking_error': self.tracking_error,
        }
