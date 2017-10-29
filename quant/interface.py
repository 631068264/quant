#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/18 09:43
@annotation = ''
"""
import abc

from six import with_metaclass


class AbstractDataSource(with_metaclass(abc.ABCMeta)):
    """数据源接口"""

    @abc.abstractmethod
    def get_calendar(self, instrument, frequency):
        pass

    @abc.abstractmethod
    def get_bar(self, instrument, dt, frequency):
        pass

    @abc.abstractmethod
    def history_bar(self, instrument, frequency, bar_count, dt, fields):
        pass

    @abc.abstractmethod
    def get_calendar_range(self, instrument, frequency):
        pass


class AbstractBroker(with_metaclass(abc.ABCMeta)):
    """交易代理 处理所有的order trade"""

    @abc.abstractmethod
    def get_portfolio(self):
        pass

    @abc.abstractmethod
    def submit_order(self, order):
        pass

    @abc.abstractmethod
    def cancel_order(self, order):
        pass

    @abc.abstractmethod
    def get_open_orders(self, symbol):
        pass


class AbstractEventSource(with_metaclass(abc.ABCMeta)):
    """事件源"""

    @abc.abstractmethod
    def events(self, start_date, end_date, frequency):
        pass


class AbstractMod(with_metaclass(abc.ABCMeta)):
    """扩展模块"""

    @abc.abstractmethod
    def start(self, env, mod_config):
        pass

    @abc.abstractmethod
    def stop(self, *args, **kwargs):
        pass


class AbstractValidator(with_metaclass(abc.ABCMeta)):
    """检验器"""

    @abc.abstractclassmethod
    def can_submit_order(self, account, order):
        pass

    @abc.abstractclassmethod
    def can_cancel_order(self, account, order):
        pass


class AbstractStrategy(with_metaclass(abc.ABCMeta)):
    """策略"""

    @abc.abstractmethod
    def init(self, context):
        pass

    @abc.abstractmethod
    def before_trading(self, context):
        pass

    @abc.abstractmethod
    def handle_bar(self, context, bar):
        raise NotImplementedError

    @abc.abstractmethod
    def after_trading(self, context):
        pass


class BaseStrategy(AbstractStrategy):
    def handle_bar(self, context, bar):
        raise NotImplementedError

    def before_trading(self, context):
        pass

    def after_trading(self, context):
        pass

    def init(self, context):
        pass
