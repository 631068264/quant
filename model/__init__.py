#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 15:27
@annotation = ''
"""
import collections

import numpy as np
import six


def id_gen(start=1):
    """获取id"""
    i = start
    while True:
        yield i
        i += 1


def repr_dict(self):
    return "%s(%s)" % (
        self.__class__.__name__,
        {k.replace("_", "", 1) if k.startswith("_") else k: v for k, v in six.iteritems(self.__dict__)})


def safe_float(value, ndigits=3):
    if isinstance(value, (float, np.float64, np.float32, np.float16, np.float)):
        return round(value, ndigits)

    return value


class AttrDict(object):
    def __init__(self, dic=None):
        self.__dict__ = dic if dic is not None else dict()

        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, dict):
                self.__dict__[k] = AttrDict(v)

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__dict__)

    def __iter__(self):
        return self.__dict__.__iter__()

    def update(self, other):
        AttrDict._update_dict_recursive(self, other)

    def items(self):
        return six.iteritems(self.__dict__)

    iteritems = items

    @staticmethod
    def _update_dict_recursive(target, other):
        if isinstance(other, AttrDict):
            other = other.__dict__
        if isinstance(target, AttrDict):
            target = target.__dict__

        for k, v in six.iteritems(other):
            if isinstance(v, collections.Mapping):
                r = AttrDict._update_dict_recursive(target.get(k, {}), v)
                target[k] = r
            else:
                target[k] = other[k]
        return target

    def convert_to_dict(self):
        result_dict = {}
        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, AttrDict):
                v = v.convert_to_dict()
            result_dict[k] = v
        return result_dict


instrument_info = {
    # 修改_get_all_instrument/update_bundle
    "okcn": [
        {
            "pair": "btc_cny",
            "fee": 0.2,
            "min_amount": 0.01,
            "table_format": "okcn_btc_cny_%s",
        },
        {
            "pair": "ltc_cny",
            "fee": 0.2,
            "min_amount": 0.1,
            "table_format": "okcn_ltc_cny_%s",
        },
    ],
}

from model.account import *
from model.bar import *
from model.broker import *
from model.const import *
from model.context import *
from model.data_source import *
from model.environment import *
from model.event_source import *
from model.events import *
from model.exception import *
from model.executor import *
from model.instrument import *
from model.interface import *
from model.mod import *
from model.order import *
from model.portfolio import *
from model.position import *
