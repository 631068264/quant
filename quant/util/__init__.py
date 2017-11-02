#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 10:15
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


def error_msg():
    import traceback
    return traceback.format_exc()


def import_mod(mod_name):
    try:
        from importlib import import_module
        return import_module(mod_name)
    except Exception as e:
        pass
