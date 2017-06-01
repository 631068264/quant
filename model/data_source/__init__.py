#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/18 10:13
@annotation = ''
"""
import os
from functools import lru_cache

import bcolz
import click
import numpy as np
import pandas as pd

from base import dao
from base.smartsql import QS, T, F
from model import const, instrument_info
from model.instrument import get_all_instrument

INSTRUMENT_DICT = get_all_instrument(instrument_info=instrument_info)
# TODO fix bundle path
BUNDLE_DIR = os.path.join(os.path.dirname(__file__), "bundle")


def update_bundle():
    progress_bar = click.progressbar(length=len(INSTRUMENT_DICT.values()) * len(const.FREQUENCY.ALL),
                                     label="Bundle updating...")

    def save(df):
        resample_data = df
        for frequency in const.FREQUENCY.ALL:
            if not frequency == const.FREQUENCY.ONE_MINUTE:
                resample_data = _resample(df, frequency)
            rootdir = os.path.join(BUNDLE_DIR, instrument.bar_name(frequency))
            bcolz.ctable.fromdataframe(resample_data, rootdir=rootdir, mode="w")
            bcolz.carray(resample_data["date"].values, rootdir=rootdir + ".datetime", mode="w")
            progress_bar.update(1)

    db_kline = dao.kline()
    if not os.path.exists(BUNDLE_DIR):
        os.mkdir(BUNDLE_DIR)

    for instrument in INSTRUMENT_DICT.values():
        # TODO fix limit
        data = QS(db_kline).table(getattr(T, instrument.bar_name(const.FREQUENCY.ONE_MINUTE))) \
            .order_by(F.date, desc=True).limit(0, 2000).select("*")
        df = pd.DataFrame(data).sort_values(by="date")
        df = _fill_df(df)
        save(df)
    progress_bar.render_finish()


@lru_cache(None)
def get_all_bar(instrument, frequency):
    try:
        bar_name = instrument.bar_name(frequency)
        root_dir = os.path.join(BUNDLE_DIR, bar_name)
        zf = bcolz.open(root_dir, "r")

        fields = zf.names
        fields.remove("date")
        dtype = np.dtype([("datetime", pd.Timestamp)] + [(f, np.dtype('float64')) for f in fields])
        result = np.empty(shape=(zf.size,), dtype=dtype)
        for field in fields:
            result[field] = zf.cols[field]
        result["datetime"] = np.array([pd.Timestamp(date) for date in zf.cols["date"]], dtype=pd.Timestamp)
        return result
    except Exception as e:
        raise e


def get_trade_date(instrument, frequency):
    try:
        bar_name = instrument.bar_name(frequency)
        root_dir = os.path.join(BUNDLE_DIR, bar_name) + ".datetime"
        zf = bcolz.open(root_dir, "r")
        result = np.array([pd.Timestamp(date) for date in zf], dtype=pd.Timestamp)
        return result
    except Exception as e:
        raise e


def _fill_df(df):
    df.set_index("date", inplace=True)
    # ohlc fillna
    close = df['close'].fillna(method='ffill')
    df = df.apply(lambda x: x.fillna(close))
    # sum fill0
    df['volume'].replace(to_replace=0, method="ffill", inplace=True)
    df["date"] = df.index
    return df


def _resample(df, frequency):
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


from model.data_source.base_source import BaseDataSource
from model.data_source.data_proxy import DataProxy
