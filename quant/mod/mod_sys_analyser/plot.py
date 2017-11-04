#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/27 16:00
@annotation = ''
"""


def generate_plot(result_dict, show_windows=True, savefile=None):
    import os
    from matplotlib import rcParams, gridspec, ticker, image as mpimg, pyplot as plt
    from matplotlib.font_manager import findfont, FontProperties
    import numpy as np

    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = [
                                      u'Microsoft Yahei',
                                      u'Heiti SC',
                                      u'Heiti TC',
                                      u'STHeiti',
                                      u'WenQuanYi Zen Hei',
                                      u'WenQuanYi Micro Hei',
                                      u"文泉驿微米黑",
                                      u'SimHei',
                                  ] + rcParams['font.sans-serif']
    rcParams['axes.unicode_minus'] = False

    use_chinese_fonts = True
    font = findfont(FontProperties(family=['sans-serif']))
    if "/matplotlib/" in font:
        use_chinese_fonts = False

    summary = result_dict["summary"]

    title = u"策略分析"

    portfolio = result_dict["portfolio"]
    benchmark_portfolio = result_dict.get("benchmark_portfolio")

    index = portfolio.index

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

    max_dd_info = "MaxDD  {}~{}, {} days".format(index[max_dd_start], index[max_dd_end],
                                                 (index[max_dd_end] - index[max_dd_start]).days)
    max_dd_info += "\nMaxDDD {}~{}, {} days".format(index[max_ddd_start_day], index[max_ddd_end_day],
                                                    (index[max_ddd_end_day] - index[max_ddd_start_day]).days)

    plt.style.use('ggplot')

    red = "#aa4643"
    blue = "#4572a7"
    black = "#000000"

    plots_area_size = 0
    if "plots" in result_dict:
        plots_area_size = 5

    figsize = (18, 6 + int(plots_area_size * 0.9))
    plt.figure(title, figsize=figsize)
    max_height = 10 + plots_area_size
    gs = gridspec.GridSpec(max_height, 8)

    # # draw logo
    # ax = plt.subplot(gs[:3, -1:])
    # ax.axis("off")
    # filename = os.path.join(os.path.dirname(os.path.realpath(rqalpha.__file__)), "resource")
    # filename = os.path.join(filename, "ricequant-logo.png")
    # img = mpimg.imread(filename)
    # ax.imshow(img, interpolation="nearest")
    # ax.autoscale_view()

    # draw risk and portfolio

    font_size = 12
    value_font_size = 11
    label_height, value_height = 0.8, 0.6
    label_height2, value_height2 = 0.35, 0.15

    fig_data = [
        (0.00, label_height, value_height, u"收益率", "{0:.3%}".format(summary["total_returns"]), red, black),
        (0.15, label_height, value_height, u"年化收益率", "{0:.3%}".format(summary["annualized_returns"]), red,
         black),
        (0.00, label_height2, value_height2, u"基准收益率",
         "{0:.3%}".format(summary.get("benchmark_total_returns", 0)), blue,
         black),
        (0.15, label_height2, value_height2, u"基准年化收益率",
         "{0:.3%}".format(summary.get("benchmark_annualized_returns", 0)),
         blue, black),

        (0.30, label_height, value_height, u"Alpha", "{0:.4f}".format(summary["alpha"]), black, black),
        (0.40, label_height, value_height, u"Beta", "{0:.4f}".format(summary["beta"]), black, black),
        (0.55, label_height, value_height, u"Sharpe", "{0:.4f}".format(summary["sharpe"]), black, black),
        (0.70, label_height, value_height, u"Sortino", "{0:.4f}".format(summary["sortino"]), black, black),
        (
            0.85, label_height, value_height, u"Information Ratio", "{0:.4f}".format(summary["information_ratio"]),
            black,
            black),

        (0.30, label_height2, value_height2, u"Volatility", "{0:.4f}".format(summary["volatility"]), black, black),
        (
            0.40, label_height2, value_height2, u"MaxDrawdown", "{0:.3%}".format(summary["max_drawdown"]), black,
            black),
        (0.55, label_height2, value_height2, u"Tracking Error", "{0:.4f}".format(summary["tracking_error"]), black,
         black),
        (0.70, label_height2, value_height2, u"Downside Risk", "{0:.4f}".format(summary["downside_risk"]), black,
         black),
    ]

    ax = plt.subplot(gs[:3, :-1])
    ax.axis("off")
    for x, y1, y2, label, value, label_color, value_color in fig_data:
        ax.text(x, y1, label, color=label_color, fontsize=font_size)
        ax.text(x, y2, value, color=value_color, fontsize=value_font_size)
    for x, y1, y2, label, value, label_color, value_color in [
        (0.85, label_height2, value_height2, "MaxDD/MaxDDD", max_dd_info, black, black)]:
        ax.text(x, y1, label, color=label_color, fontsize=font_size)
        ax.text(x, y2, value, color=value_color, fontsize=8)

    # strategy vs benchmark
    ax = plt.subplot(gs[4:10, :])

    ax.get_xaxis().set_minor_locator(ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(ticker.AutoMinorLocator())
    ax.grid(b=True, which='minor', linewidth=.2)
    ax.grid(b=True, which='major', linewidth=1)

    # plot two lines
    ax.plot(portfolio["unit_net_value"] - 1.0, label=u"strategy", alpha=1, linewidth=2, color=red)
    if benchmark_portfolio is not None:
        ax.plot(benchmark_portfolio["unit_net_value"] - 1.0, label=u"benchmark", alpha=1, linewidth=2, color=blue)

    # plot MaxDD/MaxDDD
    ax.plot([index[max_dd_end], index[max_dd_start]], [rt[max_dd_end] - 1.0, rt[max_dd_start] - 1.0],
            'v', color='Green', markersize=8, alpha=.7, label=u"MaxDrawdown")
    ax.plot([index[max_ddd_start_day], index[max_ddd_end_day]],
            [rt[max_ddd_start_day] - 1.0, rt[max_ddd_end_day] - 1.0], 'D', color='Blue', markersize=8, alpha=.7,
            label=u"MaxDDD")

    # place legend
    leg = plt.legend(loc="best")
    leg.get_frame().set_alpha(0.5)

    # manipulate axis
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.2f}%'.format(x * 100) for x in vals])

    # plot user plots
    if "plots" in result_dict:
        plots_df = result_dict["plots"]

        ax2 = plt.subplot(gs[11:, :])
        for column in plots_df.columns:
            ax2.plot(plots_df[column], label=column)

        leg = plt.legend(loc="best")
        leg.get_frame().set_alpha(0.5)

    if show_windows:
        plt.show()

    if savefile:
        fnmame = savefile
        if os.path.isdir(savefile):
            fnmame = os.path.join(savefile, "{}.png".format(summary["strategy_name"]))
        plt.savefig(fnmame, bbox_inches='tight')
