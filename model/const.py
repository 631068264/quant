#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 21:34
@annotation = ''
"""
from enum import Enum


class ACCOUNT_TYPE(Enum):
    # TODO:FUTURE
    SPOT = "SPOT"
    FUTURE = "FUTURE"
    BENCHMARK = "BENCHMARK"


class SIDE(Enum):
    BUY = "BUY"
    SELL = "SELL"


class ORDER_TYPE(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class ORDER_STATUS(Enum):
    PENDING_NEW = "PENDING_NEW"
    ACTIVE = "ACTIVE"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    PENDING_CANCEL = "PENDING_CANCEL"
    CANCELLED = "CANCELLED"


class RUN_TYPE(Enum):
    BACKTEST = "BACKTEST"
    PAPER_TRADING = "PAPER_TRADING"
    LIVE_TRADING = 'LIVE_TRADING'


def enum_to_str(v):
    return v.name


def str_to_enum(enum_class, s):
    return enum_class.__members__[s].value


"""
Base Data Source
"""


class PERIOD(object):
    ONE_MINUTE = 1
    THREE_MINUTE = 3
    FIVE_MINUTE = 5
    QUARTER_HOUR = 15
    HALF_HOUR = 30
    HOUR = 60
    TWO_HOUR = 120
    FOUR_HOUR = 240
    SIX_HOUR = 360
    TWELVE_HOUR = 720
    DAY = 1440

    ALL = [
        ONE_MINUTE, THREE_MINUTE, FIVE_MINUTE, QUARTER_HOUR,
        HALF_HOUR, HOUR, TWO_HOUR, FOUR_HOUR, SIX_HOUR,
        TWELVE_HOUR, DAY,
    ]


class PDMINUTE(object):
    NAME_DICT = {
        PERIOD.ONE_MINUTE: "1min",
        PERIOD.THREE_MINUTE: "3min",
        PERIOD.FIVE_MINUTE: "5min",
        PERIOD.QUARTER_HOUR: "15min",
        PERIOD.HALF_HOUR: "30min",
        PERIOD.HOUR: "1H",
        PERIOD.TWO_HOUR: "2H",
        PERIOD.FOUR_HOUR: "4H",
        PERIOD.SIX_HOUR: "6H",
        PERIOD.TWELVE_HOUR: "12H",
        PERIOD.DAY: "1D",
    }
