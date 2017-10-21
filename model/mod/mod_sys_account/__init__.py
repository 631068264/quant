#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/20 11:14
@annotation = ''
"""
__config__ = {}


def load_mod():
    from .mod import AccountMod
    return AccountMod()
