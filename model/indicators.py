#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/31 18:16
@annotation = ''
"""
import numpy as np
import talib as ta
from talib import MA_Type


def MA(close, period, matype=MA_Type.SMA):
    return ta.MA(close, timeperiod=period, matype=matype)


def EMA(close, period):
    return MA(close, period, MA_Type.EMA)


def RSI(close, period):
    return ta.RSI(close, timeperiod=period)


def BOLL(close, period):
    bbands = ta.BBANDS(close, timeperiod=period)
    return {
        "upper": bbands[0],
        "mid": bbands[1],
        "lower": bbands[2],
    }


def MACD(close, fast_period=12, slow_period=26, signal_period=9):
    dif, dea, macd = ta.MACD(
        close, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
    return dif, dea, macd


def KDJ(high, low, close, N=9, M1=3, M2=3):
    llv = _lv(low, N)
    hhv = _hv(high, N)
    rsv = ((close - llv) / (hhv - llv)) * 100
    k = EMA(rsv, M1 * 2 - 1)
    d = EMA(k, M2 * 2 - 1)
    j = 3 * k - 2 * d
    return k, d, j


def _rolling_window(a, window):
    '''
    copy from http://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
    '''
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def _lv(a, window):
    return np.min(_rolling_window(a, window), 1)


def _hv(a, window):
    return np.max(_rolling_window(a, window), 1)
