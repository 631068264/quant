#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 22:38
@annotation = ''
"""
from quant.const import SIDE, ACCOUNT_TYPE
from quant.interface import AbstractValidator


class CashValidator(AbstractValidator):
    def __init__(self, env):
        self._env = env

    def _crypto_validator(self, account, order):
        if order.side == SIDE.SELL:
            return True
        # 检查可用资金是否充足
        cost_money = order.price * order.amount
        if cost_money <= account.cash:
            return True

        order.reject(
            "Order Rejected: not enough money to buy {symbol}, needs {cost_money:.2f}, "
            "cash {cash:.2f}".format(
                symbol=order.symbol,
                cost_money=cost_money,
                cash=account.cash,
            )
        )
        return False

    def can_submit_order(self, account, order):
        if account.type == ACCOUNT_TYPE.CRYPTO.name:
            return self._crypto_validator(account, order)
        else:
            raise NotImplementedError

    def can_cancel_order(self, account, order):
        return True
