#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 15:27
@annotation = ''
"""
import collections

import six


def id_gen(start=1):
    """获取id"""
    i = start
    while True:
        yield i
        i += 1


def safe_float(value, ndigits=3):
    if isinstance(value, (float, np.float64, np.float32, np.float16, np.float)):
        return round(value, ndigits)

    return value


class AttrDict(object):
    def __init__(self, dic=None):
        self.__dict__ = dic if dic is not None else dict()

        for k, v in six.iteritems(self.__dict__):
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


from quant.modle.bar import *
from quant.const import *
from quant.context import *
from quant.data_source import *
from quant.environment import *
from quant.events import *
from quant.util.exception import *
from quant.executor import *
from quant.modle.instrument import *
from quant.interface import *
from quant.mod import *
from quant.modle.order import *
from quant.modle.portfolio import *
