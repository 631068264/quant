#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/15 21:12
@annotation = ''
"""
from quant.const import ACCOUNT_TYPE, SIDE
from quant.environment import Environment
from quant.events import EVENT
from quant.modle.base_account import BaseAccount


class CryptoAccount(BaseAccount):
    def __init__(self, cash, positions, register_event=True):
        super(CryptoAccount, self).__init__(cash, positions, register_event)
        self.trade_cost = 0

    @property
    def type(self):
        return ACCOUNT_TYPE.CRYPTO.name

    @property
    def total_value(self):
        return self.total_market_value + self.total_cash

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        # 仓位控制
        event_bus.add_listener(EVENT.TRADE, self._on_trade)
        event_bus.add_listener(EVENT.ORDER_PENDING_NEW, self._on_order_pending_new)
        event_bus.add_listener(EVENT.ORDER_CANCELLATION_PASS, self._on_order_cancel)
        event_bus.add_listener(EVENT.ORDER_UNSOLICITED_UPDATE, self._on_order_cancel)
        event_bus.add_listener(EVENT.ORDER_CREATION_REJECT, self._on_order_cancel)
        # 结算
        event_bus.add_listener(EVENT.SETTLEMENT, self._on_settlement)

    def _on_order_pending_new(self, event):
        if event.account != self:
            return
        order = event.order
        position = self.positions.get(order.symbol, None)

        if position is not None:
            position.on_order_pending_new(order)
        if order.side == SIDE.BUY:
            self.frozen_cash += order.price * order.amount

    def _on_order_cancel(self, event):
        if event.account != self:
            return
        order = event.order
        position = self.positions[order.symbol]
        position.on_order_cancel(order)
        if order.side == SIDE.BUY:
            self.frozen_cash -= order.price * order.unfilled_amount

    def _on_trade(self, event):
        if event.account != self:
            return
        trade = event.trade
        position = self.positions[trade.symbol]
        position.apply_trade(trade)

        self.trade_cost += abs(trade.price - trade.frozen_price) + trade.amount * trade.price * trade.fee
        if trade.side == SIDE.BUY:
            self.total_cash -= trade.price * trade.amount
            self.frozen_cash -= trade.frozen_price * trade.amount
        else:
            self.total_cash += trade.price * trade.amount * (1 - trade.fee)

    def _on_settlement(self, event):
        for position in list(self.positions.values()):
            # if position.amount != 0:
            #     self.total_cash += position.market_value
            self.positions.pop(position.symbol, None)
        self.trade_cost = 0

    # def _update_last_price(self, event):
    #     for position in self.positions.values():
    #         position.update_last_price()
