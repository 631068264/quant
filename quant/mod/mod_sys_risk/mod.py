#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/21 23:39
@annotation = ''
"""
from quant import AbstractMod
from .validator.positon_validator import PositionValidator
from .validator.price_validator import PriceValidator
from .validator.cash_validator import CashValidator


class RiskManagerMod(AbstractMod):
    def start(self, env, mod_config):
        if mod_config.validate_price:
            env.add_validator(PriceValidator(env))
        # if mod_config.validate_is_trading:
        #     env.add_validator(IsTradingValidator(env))
        if mod_config.validate_cash:
            env.add_validator(CashValidator(env))
        if mod_config.validate_position:
            env.add_validator(PositionValidator())

    def stop(self, *args, **kwargs):
        pass
