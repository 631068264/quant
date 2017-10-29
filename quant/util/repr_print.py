#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/23 10:19
@annotation = ''
"""
import six


def repr_dict(self):
    return "%s(%s)" % (
        self.__class__.__name__,
        {k.replace("_", "", 1) if k.startswith("_") else k: v for k, v in six.iteritems(self.__dict__)})
