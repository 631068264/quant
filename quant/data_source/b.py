#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2019-04-02 12:14
@annotation = ''
"""
import os

import numpy as np
import pandas as pd
from base import dao
from base.smartsql import QS, T, F

signal_db = dao.signal()
kline_db = dao.kline()

BUNDLE_DIR = os.path.join(os.path.dirname(__file__), "bundle")
HDF5_COMP_LEVEL = 4
HDF5_COMP_LIB = 'blosc'
# pair = 'binance_bcc_btc'
pair = 'okfuture_btc_usd_this_week'

def save_h5(key, value):
    h5_file_path = os.path.join(BUNDLE_DIR, pair + ".h5")
    with pd.HDFStore(h5_file_path, complevel=HDF5_COMP_LEVEL, complib=HDF5_COMP_LIB) as h5:
        h5.put(key, value)


def get_h5(key):
    h5_file_path = os.path.join(BUNDLE_DIR, pair + ".h5")
    return pd.read_hdf(h5_file_path, key)

k_period = 15
# rows = QS(signal_db).table(T.okbtcusd15).group_by(F.signal_type).select(
#     F.signal_type)
# print(rows)
#
# case_sql_format = """
# ,CASE  WHEN signal_type='{signal_type}' and op_type='buy' THEN 1 WHEN  signal_type='{signal_type}' and op_type='sell' THEN -1  ELSE 0 END as {signal_type}
# """
# feature_sql= """
# SELECT  k_time
# {case_sql}
# FROM signal15
#
# GROUP BY k_time
# """
# case_sql = ''
# for r in rows:
#     case_sql+=case_sql_format.format(signal_type=r.signal_type)
# print(case_sql)

# signal_db = dao.signal()
# kline_db = dao.kline()
#
# rows = QS(signal_db).table(T.ok15feature).select('*')
# df = pd.DataFrame(rows)
# save_h5('x',df)
#
#
#
# rows = QS(kline_db).table(T.okfuture_btc_usd_15_this_week).where(
#     (F.date >= '2017-08-10 09:35:00') & (F.date <= '2017-12-29 09:30:00')).select(F.date, F.close)
#
# df = pd.DataFrame(rows)
# df['change'] = df['close'].diff()
#
#
# def change_type(df):
#     if df['change'] is np.nan or df['change'] == 0:
#         return 0
#     elif df['change'] > 0:
#         return 1
#     elif df['change'] < 0:
#         return -1
#
#
# df['change_type'] = df.apply(change_type, axis=1)
# save_h5('y',df)

x, y = get_h5('x'), get_h5('y')
df = pd.merge(x, y, on='date', how='left')
df.fillna(0, inplace=True)

y_col = ['change','change_type']
Y = df[y_col]
save_h5('new_y',Y )

X = df.drop(columns=y_col+['date','close'],)
save_h5('new_x',X )
print(df.info())