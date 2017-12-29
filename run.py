#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/28 09:15
@annotation = ''
"""

import click
from quant.util.logger import sys_log

from quant import const, util
from quant.context import Context
from quant.data_source import bar_store
from quant.environment import Environment
from quant.events import Event, EVENT
from quant.executor import Executor
from quant.mod import ModHandler
from quant.strategy import Strategy


@click.group()
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def update_bundle():
    """下载历史数据"""
    bar_store.update_bundle()


@cli.command()
def test_strategy():
    pass


def _adjust_env(env):
    base_config = env.config.base
    frequency = base_config.frequency

    # adjust trade dates
    benchmark_symbol = base_config.benchmark
    origin_start_date, origin_end_date = base_config.start_date, base_config.end_date
    start, end = env.get_calendar_range(benchmark_symbol, frequency)

    assert start <= origin_end_date and origin_start_date <= end, '回测时间范围不在数据范围 data范围{%s,%s}' % (start, end)
    base_config.start_date = max(start, origin_start_date)
    base_config.end_date = min(end, origin_end_date)
    base_config.trading_calendar = env.get_calendar(benchmark_symbol,
                                                    frequency,
                                                    base_config.start_date,
                                                    base_config.end_date)
    assert len(base_config.trading_calendar) != 0
    base_config.start_date = base_config.trading_calendar[0]
    base_config.end_date = base_config.trading_calendar[-1]


def run(config, kwargs):
    user_funcs = {
        'init': kwargs.init,
        'handle_bar': kwargs.handle_bar,
        'before_trading': kwargs.before_trading,
        'after_trading': kwargs.after_trading,
    }
    env = Environment(config)
    mod_handler = ModHandler(env)
    mod_handler.start()
    _adjust_env(env)
    try:
        context = Context()
        env.event_bus.publish_event(Event(EVENT.POST_SYSTEM_INIT))
        strategy = Strategy(env.event_bus, user_funcs, context)
        strategy.init()
        Executor(env).run()

        result = mod_handler.stop(const.EXIT_CODE.EXIT_SUCCESS)
        return result
    except Exception as e:
        sys_log.error(util.error_msg())


if __name__ == '__main__':
    cli(obj={})
