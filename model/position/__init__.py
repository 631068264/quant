#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 23:11
@annotation = ''
"""
from model.position.spot_position import SpotPosition


class Positions(dict):
    def __init__(self, position_cls):
        super(Positions, self).__init__()
        self._position_cls = position_cls

    def __missing__(self, key):
        if key not in self:
            self[key] = self._position_cls(key)
        return self[key]
