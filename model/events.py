#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/16 11:43
@annotation = ''
"""

from collections import defaultdict
from enum import Enum


class Event(object):
    def __init__(self, event, **kwargs):
        self.__dict__ = kwargs
        self.event_type = event

    def __repr__(self):
        return ' '.join('{}:{}'.format(k, v) for k, v in self.__dict__.items())


class EventBus(object):
    def __init__(self):
        self._listeners = defaultdict(list)

    def add_listener(self, event, listener):
        self._listeners[event].append(listener)

    def prepend_listener(self, event, listener):
        self._listeners[event].insert(0, listener)

    def publish_event(self, event):
        for l in self._listeners[event.event_type]:
            # 如果返回 True ，那么消息不再传递下去
            if l(event):
                break


class EVENT(Enum):
    # 系统初始化后触发
    # post_system_init()
    POST_SYSTEM_INIT = 'post_system_init'

    # 在实盘时，你可能需要在此事件后根据其他信息源对系统状态进行调整
    POST_SYSTEM_RESTORED = 'post_system_restored'

    # 策略执行完init函数后触发
    # post_user_init()
    POST_USER_INIT = 'post_user_init'

    # 执行before_trading函数前触发
    # pre_before_trading()
    PRE_BEFORE_TRADING = 'pre_before_trading'
    # 该事件会触发策略的before_trading函数
    # before_trading()
    BEFORE_TRADING = 'before_trading'
    # 执行before_trading函数后触发
    # post_before_trading()
    POST_BEFORE_TRADING = 'post_before_trading'

    # 执行handle_bar函数前触发
    # pre_bar()
    PRE_BAR = 'pre_bar'
    # 该事件会触发策略的handle_bar函数
    # bar(bar_dict)
    BAR = 'bar'
    # 执行handle_bar函数后触发
    # post_bar()
    POST_BAR = 'post_bar'

    # 执行after_trading函数前触发
    # pre_after_trading()
    PRE_AFTER_TRADING = 'pre_after_trading'
    # 该事件会触发策略的after_trading函数
    # after_trading()
    AFTER_TRADING = 'after_trading'
    # 执行after_trading函数后触发
    # post_after_trading()
    POST_AFTER_TRADING = 'post_after_trading'

    # 在scheduler执行前触发
    PRE_SCHEDULED = 'pre_scheduled'
    # 在scheduler执行后触发
    POST_SCHEDULED = 'post_scheduled'

    # 结算前触发该事件
    # pre_settlement()
    PRE_SETTLEMENT = 'pre_settlement'
    # 触发结算事件
    # settlement()
    SETTLEMENT = 'settlement'
    # 结算后触发该事件
    # post_settlement()
    POST_SETTLEMENT = 'post_settlement'

    # 创建订单
    # order_pending_new(account, order)
    ORDER_PENDING_NEW = 'order_pending_new'
    # 创建订单成功
    # order_creation_pass(account, order)
    ORDER_CREATION_PASS = 'order_creation_pass'
    # 创建订单失败
    # order_creation_reject(account, order)
    ORDER_CREATION_REJECT = 'order_creation_reject'
    # 创建撤单
    # order_pending_cancel(account, order)
    ORDER_PENDING_CANCEL = 'order_pending_cancel'
    # 撤销订单成功
    # order_cancellation_pass(account, order)
    ORDER_CANCELLATION_PASS = 'order_cancellation_pass'
    # 撤销订单失败
    # order_cancellation_reject(account, order)
    ORDER_CANCELLATION_REJECT = 'order_cancellation_reject'
    # 订单状态更新
    # order_unsolicited_update(account, order)
    ORDER_UNSOLICITED_UPDATE = 'order_unsolicited_update'

    # 成交
    # trade(accout, trade, order)
    TRADE = 'trade'

    ON_LINE_PROFILER_RESULT = 'on_line_profiler_result'
