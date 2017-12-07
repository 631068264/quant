#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/22 10:54
@annotation = ''
"""
from quant.const import SIDE, ACCOUNT_TYPE
from quant.interface import AbstractValidator


class PositionValidator(AbstractValidator):
    def _crypto_validator(self, account, order):
        if order.side == SIDE.BUY:
            return True

        position = account.positions[order.symbol]
        if order.amount <= position.sellable:
            return True

        order.reject(
            "Order Rejected: not enough stock {order_id} to sell, you want to sell {quantity},"
            " sellable {sellable}".format(
                order_id=order.order_id,
                quantity=order.amount,
                sellable=position.sellable,
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
