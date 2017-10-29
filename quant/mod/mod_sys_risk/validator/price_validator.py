#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/22 10:54
@annotation = ''
"""
from quant import AbstractValidator


class PriceValidator(AbstractValidator):
    def __init__(self, env):
        self._env = env

    def can_submit_order(self, account, order):
        return True

    def can_cancel_order(self, account, order):
        return True
