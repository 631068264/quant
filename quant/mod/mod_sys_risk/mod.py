#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/21 23:39
@annotation = ''
"""
from quant.interface import AbstractMod
from .validator.cash_validator import CashValidator
from .validator.positon_validator import PositionValidator


class RiskManagerMod(AbstractMod):
    def start(self, env, mod_config):
        if mod_config.validate_cash:
            env.add_validator(CashValidator(env))
        if mod_config.validate_position:
            env.add_validator(PositionValidator())

    def stop(self, *args, **kwargs):
        pass
