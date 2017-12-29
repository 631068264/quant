#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/19 14:35
@annotation = ''
"""
import os

dirname = lambda file_name: os.path.dirname(file_name)
lib_dir = dirname(dirname(dirname(os.path.dirname(__file__))))
__config__ = {
    'log_path': os.path.join(lib_dir, 'logs')
}


def load_mod():
    from .mod import LogMod
    return LogMod()
