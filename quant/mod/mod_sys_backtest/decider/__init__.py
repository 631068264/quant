#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/25 14:23
@annotation = ''
"""
from quant.const import ACCOUNT_TYPE
from quant.environment import Environment
from .slippage import CryptoSlippage


class SlippageDecider(object):
    def __init__(self):
        config = Environment.get_instance().config
        self.slippage = getattr(config, 'slippage', 0)
        self.deciders = {
            ACCOUNT_TYPE.CRYPTO.name: CryptoSlippage(self.slippage),
        }

    def get_trade_price(self, account_type, side, price):
        return self.deciders[account_type].get_trade_price(side, price)
