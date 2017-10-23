#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/25 15:00
@annotation = ''
"""
__config__ = {
    "record": True,
    "report_save_path": None,
    "plot": True,
    "plot_save_path": None,
}


def load_mod():
    from .mod import SettlementMod
    return SettlementMod()
