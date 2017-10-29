#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/27 15:15
@annotation = ''
"""
from collections import defaultdict


class PlotStore(object):
    def __init__(self):
        self._plots = defaultdict(dict)

    def add_plot(self, dt, series_name, value):
        self._plots[series_name][dt] = value

    def get_plots(self):
        return self._plots
