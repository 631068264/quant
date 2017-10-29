#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/20 11:19
@annotation = ''
"""
from api import export_as_api
from quant import AbstractMod
from quant.const import ACCOUNT_TYPE
from .account import CryptoAccount, BenchmarkAccount
from .api import api_crypto
from .position import CryptoPosition


class AccountMod(AbstractMod):
    def stop(self, *args, **kwargs):
        pass

    def start(self, env, mod_config):
        env.set_account(ACCOUNT_TYPE.CRYPTO.name, CryptoAccount)
        env.set_account(ACCOUNT_TYPE.BENCHMARK.name, BenchmarkAccount)

        env.set_positon(ACCOUNT_TYPE.CRYPTO.name, CryptoPosition)
        env.set_positon(ACCOUNT_TYPE.BENCHMARK.name, CryptoPosition)

        if ACCOUNT_TYPE.CRYPTO.name in env.config.base.accounts:
            # 注入股票API
            for export_name in api_crypto.__all__:
                export_as_api(getattr(api_crypto, export_name))
