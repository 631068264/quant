#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/21 23:37
@annotation = ''
"""
__config__ = {
    # 检查限价单价格是否合法
    "validate_price": True,
    # 检查标的证券是否可以交易
    "validate_is_trading": True,
    # 检查可用资金是否充足
    "validate_cash": True,
    # 检查可平仓位是否充足
    "validate_position": True,
}


def load_mod():
    from .mod import RiskManagerMod
    return RiskManagerMod()
