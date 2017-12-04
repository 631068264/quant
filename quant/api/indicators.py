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

__all__ = []


def export_as_api(func):
    __all__.append(func.__name__)
    return func


@export_as_api
def CROSS(ma1, ma2):
    """ma1 上穿 ma2"""
    return ma2[-2] > ma1[-2] and ma2[-1] < ma1[-1]


@export_as_api
def CROSS_LINE(l1, l2):
    """l1 上穿 l2"""
    if isinstance(l1, int):
        l1 = np.linspace(l1, l1, 2)
    if isinstance(l2, int):
        l2 = np.linspace(l2, l2, 2)
    return l2[-2] > l1[-2] and l2[-1] < l1[-1]


@export_as_api
def MA(close, period, matype=MA_Type.SMA):
    return ta.MA(close, timeperiod=period, matype=matype)


@export_as_api
def EMA(close, period):
    return MA(close, period, MA_Type.EMA)


@export_as_api
def RSI(close, period):
    return ta.RSI(close, timeperiod=period)


@export_as_api
def BOLL(close, period):
    bbands = ta.BBANDS(close, timeperiod=period)
    return {
        "upper": bbands[0],
        "mid": bbands[1],
        "lower": bbands[2],
    }


@export_as_api
def MACD(close, fast_period=12, slow_period=26, signal_period=9):
    dif, dea, macd = ta.MACD(
        close, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
    return dif, dea, macd


@export_as_api
def KDJ(high, low, close, N=9, M1=3, M2=3):
    llv = LLV(low, N)
    hhv = HHV(high, N)
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


def LLV(low, window):
    return np.min(_rolling_window(low, window), 1)


def HHV(high, window):
    return np.max(_rolling_window(high, window), 1)
