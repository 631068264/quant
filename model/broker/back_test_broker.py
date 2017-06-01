#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/20 21:22
@annotation = ''
"""
from model.const import ORDER_STATUS, SIDE, ORDER_TYPE
from model.events import Event, EVENT
from model.interface import AbstractBroker
from model.order import Order
from model.portfolio import init_portfolio

from model.trade import Trade


class BackTestBroker(AbstractBroker):
    def __init__(self, env):
        self._env = env
        self._open_orders = []
        self._matcher = PriceHandler(env)

        # 该事件会触发策略的before_trading函数
        self._env.event_bus.add_listener(EVENT.BEFORE_TRADING, self.before_trading)
        # 该事件会触发策略的handle_bar函数
        self._env.event_bus.add_listener(EVENT.BAR, self.on_bar)
        # 该事件会触发策略的after_trading函数
        self._env.event_bus.add_listener(EVENT.AFTER_TRADING, self.after_trading)

    def get_open_orders(self, symbol):
        if symbol is None:
            return [order for account, order in self._open_orders]
        else:
            return [order for account, order in self._open_orders if order.symbol == symbol]

    def get_portfolio(self):
        return init_portfolio(self._env)

    def cancel_order(self, order):
        account = self._env.get_account(order.symbol)
        self._env.event_bus.publish_event(Event(EVENT.ORDER_PENDING_CANCEL, account=account, order=order))
        order.cancel("{order_id} order has been cancelled by user.").format(order_id=order.order_id)
        self._env.event_bus.publish_event(Event(EVENT.ORDER_CANCELLATION_PASS, account=account, order=order))
        try:
            self._open_orders.remove((account, order))
        except ValueError:
            pass

    def submit_order(self, order: Order):
        account = self._env.get_account(order.symbol)
        self._env.event_bus.publish_event(Event(EVENT.ORDER_PENDING_NEW, account=account, order=order))
        if order.is_final():
            return
        self._open_orders.append((account, order))
        order.active()
        self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=order))
        self._match()

    def before_trading(self, event):
        for account, order in self._open_orders:
            order.active()
            self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=order))

    def after_trading(self, event):
        for account, order in self._open_orders:
            order.rejected("Order Rejected: {symbol} can not match. Market close.").format(
                symbol=order.symbol
            )
            self._env.event_bus.publish_event(Event(EVENT.ORDER_UNSOLICITED_UPDATE, account=account, order=order))

    def on_bar(self, event):
        self._matcher.update(self._env.calendar_dt, self._env.trading_dt)
        self._match()

    def _match(self, symbol=None):
        open_orders = self._open_orders
        if symbol is not None:
            open_orders = [(a, o) for (a, o) in self._open_orders if o.symbol == symbol]
        self._matcher.match(open_orders)
        final_orders = [(a, o) for a, o in self._open_orders if o.is_final()]
        self._open_orders = [(a, o) for a, o in self._open_orders if not o.is_final()]

        for account, order in final_orders:
            if order.status == ORDER_STATUS.REJECTED or order.status == ORDER_STATUS.CANCELLED:
                self._env.event_bus.publish_event(Event(EVENT.ORDER_UNSOLICITED_UPDATE, account=account, order=order))


class PriceHandler(object):
    def __init__(self, env):
        self._calendar_dt = None
        self._trading_dt = None
        self._env = env

    def update(self, calendar_dt, trading_dt):
        self._calendar_dt = calendar_dt
        self._trading_dt = trading_dt

    def match(self, open_orders):
        for account, order in open_orders:
            last_price = self._env.get_last_price(order.symbol)
            symbol = order.symbol
            instrument = self._env.get_instrument(symbol)
            if order.type == ORDER_TYPE.LIMIT:
                if order.side == SIDE.BUY and (order.price < last_price or account.cash < order.trade_cost):
                    continue
                if order.side == SIDE.SELL and \
                        (order.price > last_price or account.positions[order.symbol] < order.amount):
                    continue
            order.fill()
            trade = Trade.create_trade(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side,
                frozen_price=order.price,
                frozen_amount=order.amount,
                fee=instrument.fee,
                trade_cost=order.trade_cost,
            )
            self._env.event_bus.publish_event(Event(EVENT.TRADE, account=account, trade=trade, order=order))
