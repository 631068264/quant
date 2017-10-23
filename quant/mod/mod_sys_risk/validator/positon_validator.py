#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/22 10:54
@annotation = ''
"""
from quant import AbstractValidator, ORDER_TYPE


class PositionValidator(AbstractValidator):
    def release_order(self, account, order):
        # TODO:
        if order.type != ORDER_TYPE.LIMIT:
            return True
        return True

    def intercept_order(self, account, order):
        pass
