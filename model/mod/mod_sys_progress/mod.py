#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/25 14:26
@annotation = ''
"""
import click

from model.events import EVENT
from model.interface import AbstractMod


class ProgressMod(AbstractMod):
    def __init__(self):
        self._show = False
        self._progress_bar = None
        self._trading_length = 0
        self._env = None

    def start(self, env, mod_config):
        self._show = mod_config.show
        self._env = env
        if self._show:
            env.event_bus.add_listener(EVENT.POST_SYSTEM_INIT, self._init)
            env.event_bus.add_listener(EVENT.POST_AFTER_TRADING, self._on_after_trade)

    def _init(self, event):

        self._trading_length = len(self._env.config.base.trading_calendar)
        self.progress_bar = click.progressbar(length=self._trading_length, show_eta=False)

    def _on_after_trade(self, event):
        self.progress_bar.update(1)

    def stop(self, *args, **kwargs):
        if self._show:
            self.progress_bar.render_finish()
