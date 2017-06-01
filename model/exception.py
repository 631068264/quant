#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/23 21:06
@annotation = ''
"""


class MethodException(Exception):
    pass


class InvalidArgumentException(MethodException):
    pass


class ApplyException(MethodException):
    pass


class CashException(Exception):
    pass


class CashTooLessException(CashException):
    pass
