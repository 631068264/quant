#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/24 17:02
@annotation = ''
"""
from quant.environment import Environment
from quant.events import EVENT
from .crypto_account import CryptoAccount


class BenchmarkAccount(CryptoAccount):
    def __init__(self, cash, positions):
        super(BenchmarkAccount, self).__init__(cash, positions, True)
        self.benchmark = Environment.get_instance().config.base.benchmark

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        event_bus.prepend_listener(EVENT.SETTLEMENT, self._on_settlement)
        event_bus.prepend_listener(EVENT.PRE_BAR, self._on_bar)

    def _on_bar(self, event):
        if len(self.positions) == 0:
            instrument = Environment.get_instance().get_instrument(self.benchmark)
            price = event.bar_dict[self.benchmark].close
            position = self.positions.get_or_create(self.benchmark)
            amount = self.total_cash / price
            position.amount = amount * (1 - instrument.fee)
            position.buy_price = price
            self.total_cash -= price * amount
