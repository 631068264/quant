#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/29 08:42
@annotation = ''
"""


# TODO:
from quant.const import RUN_TYPE
from quant.interface import AbstractMod


class RealtimeMod(AbstractMod):
    def start(self, env, mod_config):
        base_config = env.config.base
        if base_config.run_type in (RUN_TYPE.PAPER_TRADING, RUN_TYPE.LIVE_TRADING):
            pass

    def stop(self, *args, **kwargs):
        pass
