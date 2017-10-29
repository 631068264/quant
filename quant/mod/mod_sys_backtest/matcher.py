#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/24 15:20
@annotation = ''
"""

from quant import ORDER_TYPE, SIDE, Event, EVENT
from quant.modle.trade import Trade
from .decider import SlippageDecider


class Matcher(object):
    def __init__(self, env):
        self._calendar_dt = None
        self._trading_dt = None
        self._env = env
        self._slippage_decider = SlippageDecider()

    def update(self, calendar_dt, trading_dt):
        self._calendar_dt = calendar_dt
        self._trading_dt = trading_dt

    def match(self, open_orders):
        for account, order in open_orders:
            symbol = order.symbol
            last_price = self._env.get_last_price(symbol)
            # instrument = self._env.get_instrument(symbol)

            if order.type == ORDER_TYPE.LIMIT:
                if order.side == SIDE.BUY and \
                        (order.price < last_price or account.cash < order.amount * order.price):
                    continue
                if order.side == SIDE.SELL and \
                        (order.price > last_price or account.positions[order.symbol] < order.amount):
                    continue

            price = self._slippage_decider.get_trade_price(account.type, order.side, last_price)
            trade = Trade.create_trade(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side,
                price=price,
                frozen_price=order.price,
                amount=order.unfilled_amount,
                fee=order.fee,
            )
            order.fill(trade)
            self._env.event_bus.publish_event(Event(EVENT.TRADE, account=account, trade=trade, order=order))
