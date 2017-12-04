#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/31 17:00
@annotation = ''
"""
import os
from functools import lru_cache

import click
import numpy as np
import pandas as pd

from base import dao
from base.smartsql import QS, T, F
from quant import const
from quant.util.config import get_all_instrument

INSTRUMENT_DICT = get_all_instrument()
# TODO fix bundle path
BUNDLE_DIR = os.path.join(os.path.dirname(__file__), "bundle")
HDF5_COMP_LEVEL = 4
HDF5_COMP_LIB = 'blosc'


def update_bundle():
    progress_bar = click.progressbar(length=len(INSTRUMENT_DICT.values()) * len(const.FREQUENCY.ALL),
                                     label="Bundle updating...")

    def resample(df, frequency):
        df.set_index("date", inplace=True)
        resample_data = df.resample(const.PDMINUTE.NAME_DICT[frequency]).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        })
        resample_data["date"] = resample_data.index
        df["date"] = df.index
        return resample_data

    def fill_df(df):
        df.set_index("date", inplace=True)
        # ohlc fillna
        close = df['close'].fillna(method='ffill')
        df = df.apply(lambda x: x.fillna(close))
        df = df.apply(pd.to_numeric)
        # sum fill0
        df['volume'].replace(to_replace=0, method="ffill", inplace=True)
        df["date"] = df.index
        return df

    def save(df, frequency):
        h5_file_path = os.path.join(BUNDLE_DIR, instrument.symbol + ".h5")
        with pd.HDFStore(h5_file_path, complevel=HDF5_COMP_LEVEL, complib=HDF5_COMP_LIB) as h5:
            bar_name = instrument.bar_name(frequency)
            h5.put(bar_name, df)
            h5.put(bar_name + 'date', df['date'])
            progress_bar.update(1)

    db_kline = dao.kline()
    if not os.path.exists(BUNDLE_DIR):
        os.mkdir(BUNDLE_DIR)

    for instrument in INSTRUMENT_DICT.values():
        # data = QS(db_kline).table(getattr(T, instrument.bar_name(const.FREQUENCY.ONE_MINUTE))) \
        #     .order_by(F.date, desc=True).limit(0, 20000).select("*")
        for frequency in const.FREQUENCY.ALL:
            data = QS(db_kline).table(getattr(T, instrument.bar_name(frequency=frequency))) \
                .order_by(F.date, desc=True).limit(0, 20000).select("date,open,high,low,close,volume")
            df = pd.DataFrame(data).sort_values(by="date")
            df = fill_df(df)
            # if frequency != const.FREQUENCY.ONE_MINUTE:
            #     df = resample(df, frequency)
            save(df, frequency)
    progress_bar.render_finish()


@lru_cache(1024)
def get_all_bar(instrument, frequency):
    try:
        h5_file_path = os.path.join(BUNDLE_DIR, instrument.symbol + ".h5")
        df = pd.read_hdf(h5_file_path, instrument.bar_name(frequency))
        fields = df.columns.values.tolist()
        fields.remove("date")
        dtype = np.dtype([("datetime", pd.Timestamp)] + [(f, np.dtype('float64')) for f in fields])
        result = np.empty(shape=(df.shape[0],), dtype=dtype)
        for field in fields:
            result[field] = df[field].values
        result["datetime"] = np.array([pd.Timestamp(date) for date in df["date"]], dtype=pd.Timestamp)
        return result
    except Exception as e:
        raise e


@lru_cache(1024)
def get_trade_date(instrument, frequency):
    try:
        h5_file_path = os.path.join(BUNDLE_DIR, instrument.symbol + ".h5")
        series = pd.read_hdf(h5_file_path, instrument.bar_name(frequency) + "date")
        result = np.array([pd.Timestamp(date) for date in series.values], dtype=pd.Timestamp)
        return result
    except Exception as e:
        raise e
