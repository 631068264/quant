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
from quant import data_source, ACCOUNT_TYPE, Portfolio
from quant.context import Context
from quant.environment import Environment
from quant.events import EVENT, Event
from quant.executor import Executor
from quant.mod import ModHandler
from quant.modle.base_position import Positions
from quant.strategy import Strategy


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


def _adjust_env(env):
    # TODO: 可以禁止benchmark
    base_config = env.config.base
    frequency = base_config.frequency

    def create_benchmark_portfolio():
        BenchmarkAccount = env.get_account(ACCOUNT_TYPE.BENCHMARK.name)
        BenchmarkPosition = env.get_position(ACCOUNT_TYPE.BENCHMARK.name)
        total_cash = sum(base_config.account.values())
        accounts = {
            ACCOUNT_TYPE.BENCHMARK.name: BenchmarkAccount(total_cash, Positions(BenchmarkPosition)),
        }
        return Portfolio(base_config.start_date, total_cash, accounts)

    # adjust benchmark
    symbol = getattr(base_config, "symbol", None)
    benchmark = getattr(base_config, "benchmark", None)
    if isinstance(symbol, six.string_types) and benchmark is None:
        base_config.benchmark = symbol
    env.benchmark_portfolio = create_benchmark_portfolio()

    # adjust trade dates
    benchmark_symbol = base_config.benchmark
    origin_start_date, origin_end_date = base_config.start_date, base_config.end_date
    start, end = env.get_calendar_range(benchmark_symbol, frequency)

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
    _adjust_env(env)
    mod_handler = ModHandler(env)
    mod_handler.start()
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
