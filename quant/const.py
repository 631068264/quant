#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 21:34
@annotation = ''
"""
from enum import Enum


class ACCOUNT_TYPE(Enum):
    CRYPTO = "CRYPTO"
    FUTURE = "FUTURE"
    BENCHMARK = "BENCHMARK"


class SIDE(Enum):
    BUY = "BUY"
    SELL = "SELL"

    NAME_DICT = {
        BUY: 1,
        SELL: -1,
    }


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


class EXIT_CODE(Enum):
    EXIT_SUCCESS = 'EXIT_SUCCESS'


def enum_to_str(v):
    return v.name


def str_to_enum(enum_class, s):
    return enum_class.__members__[s].value


"""
Base Data Source
"""


class FREQUENCY(object):
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
        FREQUENCY.ONE_MINUTE: "1min",
        FREQUENCY.THREE_MINUTE: "3min",
        FREQUENCY.FIVE_MINUTE: "5min",
        FREQUENCY.QUARTER_HOUR: "15min",
        FREQUENCY.HALF_HOUR: "30min",
        FREQUENCY.HOUR: "1H",
        FREQUENCY.TWO_HOUR: "2H",
        FREQUENCY.FOUR_HOUR: "4H",
        FREQUENCY.SIX_HOUR: "6H",
        FREQUENCY.TWELVE_HOUR: "12H",
        FREQUENCY.DAY: "1D",
    }
