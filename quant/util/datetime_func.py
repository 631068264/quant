#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 10:21
@annotation = ''
"""
import datetime
from functools import lru_cache

import pandas as pd


@lru_cache(20480)
def convert_to_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(dt, datetime.datetime):
        return dt
    if isinstance(dt, pd.Timestamp):
        return dt.to_pydatetime()
    if isinstance(dt, str):
        return datetime.datetime.strptime(dt, format)
    if not isinstance(dt, int):
        dt = int(dt)
        return datetime.datetime.fromtimestamp(dt)
