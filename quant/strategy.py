#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/17 16:21
@annotation = ''
"""
from quant.environment import Environment
from quant.events import EVENT, Event


# TODO:通过继承写策略
class Strategy(object):
    def __init__(self, event_bus, scope, ucontext):
        self._user_context = ucontext
        self._current_universe = set()

        self._init = scope.get('init', None)
        self._handle_bar = scope.get('handle_bar', None)
        self._before_trading = scope.get('before_trading', None)
        self._after_trading = scope.get('after_trading', None)

        if self._before_trading is not None:
            event_bus.add_listener(EVENT.BEFORE_TRADING, self.before_trading)
        if self._handle_bar is not None:
            event_bus.add_listener(EVENT.BAR, self.handle_bar)
        if self._after_trading is not None:
            event_bus.add_listener(EVENT.AFTER_TRADING, self.after_trading)

    @property
    def user_context(self):
        return self._user_context

    def init(self):
        if not self._init:
            return
        self._init(self._user_context)
        Environment.get_instance().event_bus.publish_event(Event(EVENT.POST_USER_INIT))

    def before_trading(self, event):
        self._before_trading(self._user_context)

    def handle_bar(self, event):
        bar_dict = event.bar_dict
        self._handle_bar(self._user_context, bar_dict)

    def after_trading(self, event):
        self._after_trading(self._user_context)
