#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/25 14:24
@annotation = ''
"""

__config__ = {
    "show": False,
}


def load_mod():
    from .mod import ProgressMod
    return ProgressMod()
