#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/28 14:18
@annotation = ''
"""
__config__ = {
    'signal': False,
}


def load_mod():
    from .mod import AnalyserMod
    return AnalyserMod()
