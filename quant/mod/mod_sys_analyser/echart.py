#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/8 10:27
@annotation = ''
"""
import numpy as np

from quant.environment import Environment
from quant.mod.mod_sys_analyser.echart_util.chart import Page, Chart
from quant.mod.mod_sys_analyser.echart_util.component import Text, Axis, KLineMakePoint

volume_index = 0


def generate_echart(result_dict=None, show_windows=True, savefile=None):
    summary = result_dict["summary"]
    portfolio = result_dict["portfolio"]
    benchmark_portfolio = result_dict.get("benchmark_portfolio")
    x_axis = portfolio.index

    # maxdrawdown
    portfolio_value = portfolio.unit_net_value * portfolio.start_cash
    xs = portfolio_value.values
    rt = portfolio.unit_net_value.values
    max_dd_end = np.argmax(np.maximum.accumulate(xs) / xs)
    if max_dd_end == 0:
        max_dd_end = len(xs) - 1
    max_dd_start = np.argmax(xs[:max_dd_end]) if max_dd_end > 0 else 0

    # maxdrawdown duration
    al_cum = np.maximum.accumulate(xs)
    a = np.unique(al_cum, return_counts=True)
    start_idx = np.argmax(a[1])
    m = a[0][start_idx]
    al_cum_array = np.where(al_cum == m)
    max_ddd_start_day = al_cum_array[0][0]
    max_ddd_end_day = al_cum_array[0][-1]

    max_dd_info = "MaxDD  {}~{}, {} days".format(x_axis[max_dd_start], x_axis[max_dd_end],
                                                 (x_axis[max_dd_end] - x_axis[max_dd_start]).days)
    max_dd_info += "\nMaxDDD {}~{}, {} days".format(x_axis[max_ddd_start_day], x_axis[max_ddd_end_day],
                                                    (x_axis[max_ddd_end_day] - x_axis[max_ddd_start_day]).days)

    red = "#aa4643"
    blue = "#4572a7"
    black = "#000000"

    font_size = 13
    value_font_size = 12
    label_height, value_height = 10, 40
    label_height2, value_height2 = 60, 90
    title = []
    fig_data = [
        ('15%', label_height, value_height, u"收益率", "{0:.3%}".format(summary["total_returns"]), red, black),
        ('15%', label_height2, value_height2, u"基准收益率", "{0:.3%}".format(summary.get("benchmark_total_returns", 0)),
         blue, black),

        ('22%', label_height, value_height, u"年化收益率", "{0:.3%}".format(summary["annualized_returns"]),
         red, black),
        ('22%', label_height2, value_height2, u"基准年化收益率",
         "{0:.3%}".format(summary.get("benchmark_annualized_returns", 0)), blue, black),

        ('32%', label_height, value_height, u"Alpha", "{0:.4f}".format(summary["alpha"]), black, black),
        ('32%', label_height2, value_height2, u"Volatility", "{0:.4f}".format(summary["volatility"]), black, black),

        ('40%', label_height, value_height, u"Beta", "{0:.4f}".format(summary["beta"]), black, black),
        ('40%', label_height2, value_height2, u"MaxDrawdown", "{0:.3%}".format(summary["max_drawdown"]), black, black),

        ('50%', label_height, value_height, u"Sharpe", "{0:.4f}".format(summary["sharpe"]), black, black),
        ('50%', label_height2, value_height2, u"Tracking Error", "{0:.4f}".format(summary["tracking_error"]), black,
         black),

        ('60%', label_height, value_height, u"Sortino", "{0:.4f}".format(summary["sortino"]), black, black),
        ('60%', label_height2, value_height2, u"Downside Risk", "{0:.4f}".format(summary["downside_risk"]), black,
         black),

        ('70%', label_height, value_height, u"Information Ratio", "{0:.4f}".format(summary["information_ratio"]),
         black, black),
    ]
    for x, y1, y2, label, value, label_color, value_color in fig_data:
        title.append(Text(x, y1, label, color=label_color, fontsize=font_size))
        title.append(Text(x, y2, value, color=value_color, fontsize=value_font_size))
    for x, y1, y2, label, value, label_color, value_color in [
        ('70%', label_height2, value_height2, "MaxDD/MaxDDD", max_dd_info, black, black)]:
        title.append(Text(x, y1, label, color=label_color, fontsize=font_size))
        title.append(Text(x, y2, value, color=value_color, fontsize=8))

    page = Page()
    # title
    title_chart = Chart(title=title, width=1000, height=180, show_xaxis=False, show_yaxis=False)
    page.add(title_chart)

    # line
    line = Chart(title=Text(text='收益曲线'), animation=False, dataZoom=[
        {
            'type': 'slider',
            'xAxisIndex': [0],
        },
        {
            'type': 'inside',
            'xAxisIndex': [0],
        },
    ])
    line.set_tooltip(**{
        'trigger': 'axis',
        'axisPointer': {'type': 'cross'},
    })
    line.set_xaxis(Axis(data=x_axis, type='category'))
    # plot strategy and benchmark
    line.line(label='strategy', data=portfolio["unit_net_value"] - 1.0, color=red)
    if benchmark_portfolio is not None:
        line.line(label='benchmark', data=benchmark_portfolio["unit_net_value"] - 1.0, color=blue)
    # plot MaxDD/MaxDDD
    line.line(label='MaxDrawdown', data=[
        [x_axis[max_dd_end], rt[max_dd_end] - 1.0],
        [x_axis[max_dd_start], rt[max_dd_start] - 1.0],
    ], color='green', smooth=False, fill=True, opacity=0.1)
    line.line(label='MaxDDD', data=[
        [x_axis[max_ddd_start_day], rt[max_ddd_start_day] - 1.0],
        [x_axis[max_ddd_end_day], rt[max_ddd_end_day] - 1.0],
    ], color='blue', smooth=False, fill=True, opacity=0.1)
    page.add(line)

    # kline
    upcolor, downcolor = '#52b986', '#ec4d5c'
    buycolor, sellcolor = '#018ffe', '#cc46ed'

    k_bar = Environment.get_instance().get_plot_bar()
    trade_mark, buy_count, sell_count = KLineMakePoint(mark_size=8).mark_point(result_dict['trades'])
    k_count = len(k_bar)

    label_height, value_height = 10, 40
    title = []
    fig_data = [
        ('15%', label_height, value_height, u"buy", "{}/{} {:.3f}".format(buy_count, k_count, buy_count / k_count),
         buycolor, black),
        ('25%', label_height, value_height, u"sell", "{}/{} {:.3f}".format(sell_count, k_count, sell_count / k_count),
         sellcolor, black),
        ('35%', label_height, value_height, u"all", "{}/{} {:.3f}".format(
            buy_count + sell_count, k_count, (buy_count + sell_count) / k_count), black, black),
    ]
    for x, y1, y2, label, value, label_color, value_color in fig_data:
        title.append(Text(x, y1, label, color=label_color, fontsize=font_size))
        title.append(Text(x, y2, value, color=value_color, fontsize=value_font_size))
    title_chart = Chart(title=title, height=60, show_xaxis=False, show_yaxis=False)
    page.add(title_chart)

    kline_chart = Chart(title=Text(text='K线交易'), height=500, animation=False, show_legend=False,
                        dataZoom=[
                            {
                                'type': 'slider',
                                'xAxisIndex': [0, 1],
                                'start': 1,
                                'end': 35,
                                'top': '85%',
                            },
                            {
                                'type': 'inside',
                                'xAxisIndex': [0, 1],
                            },
                        ],
                        grid=[
                            {
                                'left': '10%',
                                'right': '8%',
                                'height': '50%'
                            },
                            {
                                'left': '10%',
                                'right': '8%',
                                'bottom': '20%',
                                'height': '15%'
                            }
                        ],
                        axisPointer={'link': {'xAxisIndex': 'all'}},
                        visualMap={
                            'show': False, 'seriesIndex': 1,
                            'pieces': [{
                                'value': 1,
                                'color': downcolor,
                            }, {
                                'value': -1,
                                'color': upcolor,
                            }]}
                        )
    kline_chart.set_tooltip(**{
        'trigger': 'axis',
        'axisPointer': {'type': 'cross'},
    })
    kline_chart.set_xaxis([
        Axis(data=x_axis, type='category'),
        Axis(data=x_axis, type='category',
             axisTick={'show': False}, axisLabel={'show': False}, gridIndex=1)
    ])
    kline_chart.set_yaxis([
        Axis(scale=True),
        Axis(scale=True, axisLabel={'show': False}, axisLine={'show': False},
             axisTick={'show': False}, splitLine={'show': False}, gridIndex=1)
    ])

    """k线"""
    kline_data = k_bar[['open', 'close', 'low', 'high']].copy().tolist()
    kline_chart.kline(label='k线', data=kline_data, upcolor=upcolor, downcolor=downcolor,
                      markPoint=trade_mark)

    def color_volume(i, data):
        """交易量上色"""
        return [i, data['volume'], 1 if data['open'] > data['close'] else -1]

    ocv = k_bar[['open', 'close', 'volume']].copy()
    volume_data = [color_volume(i, data) for i, data in enumerate(ocv)]
    kline_chart.bar('volume', data=volume_data, xAxisIndex=1, yAxisIndex=1, itemStyle={})

    page.add(kline_chart)
    page.plot()
