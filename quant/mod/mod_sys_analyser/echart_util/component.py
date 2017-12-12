#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/8 15:30
@annotation = ''
"""

import pandas as pd

from quant import const
from quant.mod.mod_sys_analyser.echart_util import json_dumps


class BaseConfig(object):
    def __repr__(self):
        return json_dumps(self.json)

    def __getitem__(self, key):
        return self.json.get(key)

    def keys(self):
        return self.json.keys()

    @property
    def json(self):
        raise NotImplementedError


class Text(BaseConfig):
    """title"""

    def __init__(self, left='auto', top='auto', text='', color='#333', fontsize=18, **kwargs):
        self.top = top
        self.left = left
        self.text = text
        self.color = color
        self.fontsize = fontsize
        self._kwargs = kwargs

    @property
    def json(self):
        config = {
            'top': self.top,
            'left': self.left,
            'text': self.text,
            'textStyle': {
                'color': self.color,
                'fontSize': self.fontsize,
            }
        }

        if self._kwargs:
            config.update(self._kwargs)

        return config


class Axis(BaseConfig):
    """坐标轴"""

    def __init__(self, type=None, data=None, name=None, **kwargs):
        if type == 'category' and data is None:
            raise RuntimeError('if type is category,you must set data')
        if type:
            assert type in ('category', 'value', 'time')
        self.type = type
        self.name = name
        self.data = data
        self._kwargs = kwargs

    @property
    def json(self):
        config = {}
        if self.type:
            config['type'] = self.type
        if self.data is not None:
            config['data'] = self.data
        if self.name:
            config['name'] = self.name

        if self._kwargs:
            config.update(self._kwargs)
        return config


class KLineMakePoint(BaseConfig):
    """K线买卖点标注"""

    def __init__(self, mark='triangle', mark_size=50, label_size=12, **kwargs):
        assert mark in ('circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow')
        self.config = {
            'symbol': mark,
            'symbolSize': mark_size,
            'label': {
                'normal': {
                    'formatter': '{c}',
                    'fontSize': label_size,
                }
            }
        }
        if kwargs:
            self.config.update(kwargs)
        self.data = []
        self.buy_trade = 0
        self.sell_trade = 0

    def add(self, df, buycolor='#018ffe', sellcolor='#cc46ed'):
        side = df['side']
        coord = [df['trading_datetime'], df['price']]
        if side == const.SIDE.BUY.value:
            label = 'buy\n{price}\n+{amount}'.format(price=df['price'], amount=df['amount'])
            color = buycolor
            mark_rotate = 0
            label_position = 'bottom'
            self.buy_trade += 1
        elif side == const.SIDE.SELL.value:
            label = '-{amount}\n{price}\nsell'.format(price=df['price'], amount=df['amount'])
            color = sellcolor
            mark_rotate = 180
            label_position = 'top'
            self.sell_trade += 1

        self._add_point(coord, label=label, color=color, mark_rotate=mark_rotate, label_position=label_position)

    def _add_point(self, coord, label='', color='auto',
                   mark_rotate=0, mark_offset=[0, 0], label_position='inside', **kwargs):
        config = {
            'symbolRotate': mark_rotate,
            'symbolOffset': mark_offset,
            'value': label,
            'coord': coord,
            'itemStyle': {
                'normal': {'color': color}
            },
            'label': {
                'normal': {
                    'position': label_position,
                    'color': color,
                }
            }
        }
        if kwargs:
            config.update(kwargs)
        self.data.append(config)

    def mark_point(self, df, buycolor='#018ffe', sellcolor='#cc46ed'):
        if isinstance(df, pd.DataFrame):
            df.apply(self.add, axis=1, buycolor=buycolor, sellcolor=sellcolor)
            return self.json, self.buy_trade, self.sell_trade

    @property
    def json(self):
        self.config['data'] = self.data
        return self.config

# class Series(BaseConfig):
#     """ Data series holding. """
#
#     def __init__(self, type, name=None, data=None, **kwargs):
#         types = (
#             'bar', 'boxplot', 'candlestick', 'chord', 'effectScatter',
#             'eventRiver', 'force', 'funnel', 'gauge', 'graph', 'heatmap',
#             'k', 'line', 'lines', 'map', 'parallel', 'pie', 'radar',
#             'sankey', 'scatter', 'tree', 'treemap', 'venn', 'wordCloud'
#         )
#         assert type in types
#         self.type = type
#         self.name = name
#         self.data = data or []
#         self._kwargs = kwargs
#
#     @property
#     def json(self):
#         json = {
#             'type': self.type,
#             'data': self.data
#         }
#         if self.name:
#             json['name'] = self.name
#         if self._kwargs:
#             json.update(self._kwargs)
#         return json
#
#
# class Toolbox(BaseConfig):
#     """ A toolbox for visitor. """
#
#     def __init__(self, orient='vertical', position=None, **kwargs):
#         assert orient in ('horizontal', 'vertical')
#         self.orient = orient
#         if not position:
#             position = ('right', 'top')
#         self.position = position
#         self._kwargs = kwargs
#
#     @property
#     def json(self):
#         """JSON format data."""
#         json = {
#             'orient': self.orient,
#             'x': self.position[0],
#             'y': self.position[1]
#         }
#         if self._kwargs:
#             json.update(self._kwargs)
#         return json
#
#
# class Legend(BaseConfig):
#     """图例"""
#
#     def __init__(self, data, orient='vertical', **kwargs):
#         self.data = data
#
#         assert orient in ('horizontal', 'vertical')
#         self.orient = orient
#         self._kwargs = kwargs
#
#     @property
#     def json(self):
#         """JSON format data."""
#         config = {
#             'data': self.data,
#             'orient': self.orient,
#         }
#
#         if self._kwargs:
#             config.update(self._kwargs)
#         return config
#
#
# class Tooltip(BaseConfig):
#     """A tooltip when hovering."""
#
#     def __init__(self, trigger='axis', **kwargs):
#         assert trigger in ('axis', 'item')
#         self.trigger = trigger
#
#         self._kwargs = kwargs
#
#     @property
#     def json(self):
#         """JSON format data."""
#         json = {
#             'trigger': self.trigger,
#         }
#         if self._kwargs:
#             json.update(self._kwargs)
#         return json
