#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/25 14:42
@annotation = ''
"""
import abc

from six import with_metaclass

from quant.const import SIDE


class BaseSlippage(with_metaclass(abc.ABCMeta)):
    @abc.abstractclassmethod
    def get_trade_price(self, side, price):
        pass


class CryptoSlippage(BaseSlippage):
    def __init__(self, slippage=0.):
        if 0 <= slippage < 1:
            self.slippage = slippage
        else:
            raise ValueError('Slippage should range [0,1)')

    def get_trade_price(self, side, price):
        return price + price * self.slippage * (1 if side == SIDE.BUY else -1)
