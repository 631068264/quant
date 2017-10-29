#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/26 17:04
@annotation = ''
"""
from __future__ import division

import numpy as np


class Risk(object):
    def __init__(self, portfolio_returns, benchmark_returns, days):
        assert (len(portfolio_returns) == len(benchmark_returns))

        self._portfolio = portfolio_returns
        self._benchmark = benchmark_returns

        self._max_drawdown = None

    @property
    def max_drawdown(self):
        """最大回撤"""
        if self._max_drawdown is not None:
            return self._max_drawdown

        if len(self._portfolio) < 1:
            self._max_drawdown = np.nan
            return np.nan

        df_cum = np.exp(np.log1p(self._portfolio).cumsum())
        max_return = np.maximum.accumulate(df_cum)
        self._max_drawdown = ((df_cum - max_return) / max_return).min()
        return abs(self._max_drawdown)
