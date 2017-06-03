#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/25 15:16
@annotation = ''
"""
from collections import defaultdict

import numpy as np
import pandas as pd
import six

from model import safe_float
from model.const import ACCOUNT_TYPE
from model.events import EVENT
from model.interface import AbstractMod
from model.mod.mod_sys_settlement.risk import Risk


def _wrap_portfolio(dt, portfolio):
    return {
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "cash": safe_float(portfolio.cash),
        "total_value": safe_float(portfolio.total_value),
        "market_value": safe_float(portfolio.total_market_value),
        "start_cash": safe_float(portfolio.start_cash),
        "static_total_value": safe_float(portfolio.static_total_value),
        "unit_net_value": safe_float(portfolio.unit_net_value, 6),
    }


def _wrap_account(dt, account):
    return {
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        'cash': safe_float(account.cash),
        'trade_cost': safe_float(account.trade_cost),
        'market_value': safe_float(account.market_value),
        'total_value': safe_float(account.total_value),
    }


def _wrap_trade(trade):
    return {
        'datetime': trade.create_dt.strftime("%Y-%m-%d %H:%M:%S"),
        'trading_datetime': trade.trade_dt.strftime("%Y-%m-%d %H:%M:%S"),
        'symbol': trade.symbol,
        'side': trade.side.name,
        'trade_id': trade.trade_id,
        'fee': trade.fee,
        'amount': safe_float(trade.amount, 8),
        'price': safe_float(trade.price),
        'order_id': trade.order_id,
        'transaction_cost': safe_float(trade.trade_cost),
    }


def _wrap_position(dt, symbol, position):
    POSITION_FIELDS_MAP = {
        ACCOUNT_TYPE.SPOT: [
            'amount', 'last_price', 'buy_price', 'market_value'
        ],
        # ACCOUNT_TYPE.FUTURE: [
        #     'margin', 'margin_rate', 'contract_multiplier', 'last_price',
        #     'buy_pnl', 'buy_margin', 'buy_quantity', 'buy_avg_open_price',
        #     'sell_pnl', 'sell_margin', 'sell_quantity', 'sell_avg_open_price'
        # ],
    }
    data = {
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        'symbol': symbol,
    }

    for f in POSITION_FIELDS_MAP[position.type]:
        data[f] = safe_float(getattr(position, f))
    return data


class SettlementMod(AbstractMod):
    def __init__(self):
        self._env = None
        self._mod_config = None
        self._enabled = False
        self._orders = []
        self._trades = []

        self._total_portfolios = []
        self._total_benchmark_portfolios = []

        self._benchmark_current_returns = []
        self._portfolio_current_returns = []

        self._sub_accounts = defaultdict(list)
        self._positions = defaultdict(list)

    def start(self, env, mod_config):
        self._env = env
        self._mod_config = mod_config
        self._enabled = self._mod_config.record or self._mod_config.plot

        if self._enabled:
            env.event_bus.add_listener(EVENT.PRE_SETTLEMENT, self._per_settlement)
            env.event_bus.add_listener(EVENT.TRADE, self._collect_trade)
            env.event_bus.add_listener(EVENT.ORDER_CREATION_PASS, self._collect_order)

    def _collect_trade(self, event):
        trade = event.trade
        self._trades.append(_wrap_trade(trade))

    def _collect_order(self, event):
        self._orders.append(event.order)

    def _per_settlement(self, event):
        dt = self._env.calendar_dt
        portfolio = self._env.portfolio
        benchmark_portfolio = self._env.benchmark_portfolio

        self._portfolio_current_returns.append(portfolio.pnl_returns)
        self._total_portfolios.append(_wrap_portfolio(dt, portfolio))

        if benchmark_portfolio is None:
            self._benchmark_current_returns.append(0)
        else:
            self._benchmark_current_returns.append(benchmark_portfolio.current_pnl_returns)
            self._total_benchmark_portfolios.append(_wrap_portfolio(dt, benchmark_portfolio))

        for account_type, account in six.iteritems(self._env.portfolio.accounts):
            self._sub_accounts[account_type].append(_wrap_account(dt, account))
            for symbol, position in six.iteritems(account.positions):
                self._positions[account_type].append(_wrap_position(dt, symbol, position))

    def stop(self, *args, **kwargs):
        if not self._enabled or len(self._total_portfolios) == 0:
            return
        base_config = self._env.config.base
        strategy_name = getattr(base_config, "strategy_name", "strategy")

        summary = {
            'strategy_name': strategy_name,
            'start_date': base_config.start_date.strftime('%Y-%m-%d'),
            'end_date': base_config.end_date.strftime('%Y-%m-%d'),
            'run_type': base_config.run_type.value,
            'spot_starting_cash': getattr(base_config, "spot_starting_cash", safe_float(0)),
            'future_starting_cash': getattr(base_config, "future_starting_cash", safe_float(0)),
            'benchmark': base_config.benchmark,
        }
        risk = Risk(np.array(self._portfolio_current_returns),
                    np.array(self._benchmark_current_returns),
                    (base_config.end_date - base_config.start_date).days + 1)

        summary.update({
            "max_drawdown": safe_float(risk.max_drawdown),
        })

        summary.update({
            'total_value': safe_float(self._env.portfolio.total_value),
            'cash': safe_float(self._env.portfolio.cash),
            'total_returns': safe_float(self._env.portfolio.pnl_returns),
            'annualized_returns': safe_float(self._env.portfolio.annualized_returns),
            'unit_net_value': safe_float(self._env.portfolio.unit_net_value),
        })

        if self._env.benchmark_portfolio:
            summary['benchmark_total_returns'] = safe_float(self._env.benchmark_portfolio.pnl_returns)
            summary['benchmark_annualized_returns'] = safe_float(
                self._env.benchmark_portfolio.annualized_returns)

        trades = pd.DataFrame(self._trades)
        if 'datetime' in trades.columns:
            trades = trades.set_index('datetime')

        df = pd.DataFrame(self._total_portfolios)
        total_portfolios = df.set_index('datetime').sort_index()

        result_dict = {
            'summary': summary,
            'trades': trades,
            'portfolio': total_portfolios,
        }

        if self._env.benchmark_portfolio is not None:
            b_df = pd.DataFrame(self._total_benchmark_portfolios)
            benchmark_portfolios = b_df.set_index('datetime').sort_index()
            result_dict['benchmark_portfolio'] = benchmark_portfolios

        if self._env.plot_store is not None:
            plots = self._env.get_plot_store().get_plots()
            plots_items = defaultdict(dict)
            for series_name, value_dict in six.iteritems(plots):
                for date, value in six.iteritems(value_dict):
                    plots_items[date][series_name] = value
                    plots_items[date]["datetime"] = date

            df = pd.DataFrame([dict_data for date, dict_data in six.iteritems(plots_items)])
            df = df.set_index("datetime").sort_index()
            result_dict["plots"] = df

        for account_type, account in six.iteritems(self._env.portfolio.accounts):
            account_name = account_type.name.lower()
            portfolios_list = self._sub_accounts[account_type]
            df = pd.DataFrame(portfolios_list)
            account_df = df.set_index("datetime").sort_index()
            result_dict["%s_account" % account_name] = account_df

            positions_list = self._positions[account_type]
            positions_df = pd.DataFrame(positions_list)
            if "date" in positions_df.columns:
                positions_df["date"] = pd.to_datetime(positions_df["date"])
                positions_df = positions_df.set_index("date").sort_index()
            result_dict["{}_positions".format(account_name)] = positions_df

        if self._mod_config.report_save_path:
            from .report import generate_report
            generate_report(result_dict, self._mod_config.report_save_path)

        if self._mod_config.plot or self._mod_config.plot_save_path:
            from .plot import generate_plot
            generate_plot(result_dict, self._mod_config.plot, self._mod_config.plot_save_path)
