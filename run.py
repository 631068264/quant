#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/28 09:15
@annotation = ''
"""
import click
import six

from base import util
from model import data_source
from model.context import Context
from model.environment import Environment
from model.events import EVENT, Event
from model.executor import Executor
from model.mod import ModHandler
from model.mod.mod_sys_account.account import create_benchmark_portfolio
from model.strategy import Strategy


@click.group()
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def update_bundle():
    """下载历史数据"""
    data_source.update_bundle()


@cli.command()
def test_strategy():
    pass


def _adjust_date(env):
    config = env.config
    frequency = config.base.frequency
    origin_start_date, origin_end_date = config.base.start_date, config.base.end_date
    start, end = env.get_calendar_range(frequency)

    config.base.start_date = max(start, origin_start_date)
    config.base.end_date = min(end, origin_end_date)

    config.base.trading_calendar = env.get_calendar(frequency, config.base.start_date, config.base.end_date)

    assert len(config.base.trading_calendar) != 0

    config.base.start_date = config.base.trading_calendar[0]
    config.base.end_date = config.base.trading_calendar[-1]
    # config.base.timezone = pytz.utc


def _check_benchmark(env):
    base_config = env.config.base
    symbol = getattr(base_config, "symbol", None)
    benchmark = getattr(base_config, "benchmark", None)

    if isinstance(symbol, six.string_types) and benchmark is None:
        base_config.benchmark = symbol
        env.benchmark_portfolio = create_benchmark_portfolio(env)

    if benchmark is None:
        return


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
    _adjust_date(env)
    _check_benchmark(env)
    try:
        context = Context()
        env.event_bus.publish_event(Event(EVENT.POST_SYSTEM_INIT))
        strategy = Strategy(env.event_bus, user_funcs, context)
        strategy.init()
        Executor(env).run()

        result = mod_handler.stop()
        return result
    except Exception as e:
        print(util.error_msg())
        # TODO:
        pass


if __name__ == '__main__':
    cli(obj={})
