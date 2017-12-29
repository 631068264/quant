#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/19 14:35
@annotation = ''
"""
from quant import const
from quant.events import EVENT
from quant.interface import AbstractMod
from quant.util import logger
from quant.util.logger import order_log


class LogMod(AbstractMod):
    def __init__(self):
        self._env = None
        self._mod_config = None

    def start(self, env, mod_config):
        self._env = env
        self._mod_config = mod_config
        self._event_bus = self._env.event_bus
        logger.init_log(dir_path=self._mod_config.log_path)
        self._event_bus.add_listener(EVENT.ORDER_CREATION_PASS, self._order_active)
        self._event_bus.add_listener(EVENT.TRADE, self._trade)

    def stop(self, *args, **kwargs):
        pass

    def _order_active(self, event):
        order = getattr(event, 'order', None)
        if order is not None:
            order_log.info('[ORDER {status}] {id} [{symbol}|{type}|{side}]: {price} {amount}'.format(
                id=order.order_id,
                symbol=order.symbol,
                type=order.type.name,
                side=order.side.name,
                price=order.price,
                amount=order.amount if order.side == const.SIDE.BUY else -order.amount,
                status=order.status.name,
            ))

    def _trade(self, event):
        order = getattr(event, 'order', None)
        if order is not None:
            order_log.info('[ORDER {status}] {id} [{symbol}]'.format(
                status=order.status.name,
                id=order.order_id,
                symbol=order.symbol,
            ))
