#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/24 15:20
@annotation = ''
"""
from quant.const import ORDER_TYPE, SIDE
from quant.events import Event, EVENT
from quant.modle.trade import Trade
from .decider import SlippageDecider


class Matcher(object):
    """撮合机制"""

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

            deal_price = order.price if order.type == ORDER_TYPE.LIMIT else last_price
            deal_price = self._slippage_decider.get_trade_price(account.type, order.side, deal_price)

            if order.type == ORDER_TYPE.LIMIT:
                if order.side == SIDE.BUY:
                    if deal_price < last_price:
                        order.message = 'Rejected [{order_price} < {last_price}]:order price too low < last price' \
                            .format(order_price=deal_price, last_price=last_price)
                        continue
                    elif account.cash < order.amount * deal_price:
                        order.message = 'Rejected [{cash} < {need_cash}] not enough cash' \
                            .format(cash=account.cash, need_cash=order.amount * deal_price)
                        continue
                if order.side == SIDE.SELL:
                    if deal_price > last_price:
                        order.message = 'Rejected [{order_price} > {last_price}]:order price too high > last price' \
                            .format(order_price=deal_price, last_price=last_price)
                        continue
                    elif account.positions[order.symbol].amount < order.amount:
                        order.message = 'Rejected [{amount} < {order_amount}]: not enough amount' \
                            .format(amount=account.positions[order.symbol].amount, order_amount=order.amount)
                        continue

            trade = Trade.create_trade(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side,
                price=deal_price,
                frozen_price=order.price,
                amount=order.unfilled_amount,
                fee=order.fee,
            )
            order.fill(trade)
            self._env.event_bus.publish_event(Event(EVENT.TRADE, account=account, trade=trade, order=order))
