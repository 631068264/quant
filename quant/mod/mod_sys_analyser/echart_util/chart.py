#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/8 17:05
@annotation = ''
"""
from quant.mod.mod_sys_analyser.echart_util import RenderMixin, json_dumps, get_chart_id, get_resource
from quant.mod.mod_sys_analyser.echart_util.component import Axis


class Base(RenderMixin):
    def __init__(self, width=800, height=400):
        self._option = {}
        self.width, self.height = width, height

    def show_config(self):
        return json_dumps(self._option, 4)

    @property
    def json(self):
        return self._option

    def _render_content(self):
        render_dict = {
            'chart_id': get_chart_id(),
            'option': json_dumps(self.json, 4),
            'width': str(self.width),
            'height': str(self.height),
        }

        with open(get_resource('content'), 'rb') as f:
            temp = f.read()
            for k, v in render_dict.items():
                temp = temp.replace(('{{ %s }}' % (k,)).encode(encoding='utf-8'), v.encode(encoding='utf-8'))
        return temp


class Chart(Base):
    def __init__(self, title=None,
                 width=800,
                 height=400, show_xaxis=True, show_yaxis=True, show_legend=True, **kwargs):
        super(Chart, self).__init__(width, height)

        self._option.update(
            title=self._check_title(title),
        )
        self._show_x_axis = show_xaxis
        self._show_y_axis = show_yaxis
        self._show_legend = show_legend

        self.x_axis = []
        self.y_axis = []
        self.series = []
        self.legend = {"data": []}
        self.tooltip = {}
        if kwargs:
            self._option.update(kwargs)

    def set_xaxis(self, axis):
        if isinstance(axis, Axis):
            self.x_axis.append(axis.json)
        elif isinstance(axis, list):
            self.x_axis += [x.json for x in axis]

    def set_yaxis(self, axis):
        if isinstance(axis, Axis):
            self.y_axis.append(axis.json)
            print(self.y_axis)
        elif isinstance(axis, list):
            self.y_axis += [x.json for x in axis]

    def set_tooltip(self, **kwargs):
        self.tooltip.update(kwargs)

    def set_legend(self, **kwargs):
        self.legend.update(kwargs)

    def line(self, label, data, color="#000", linewidth=2, opacity=1, smooth=True, fill=False, legend=True,
             xAxisIndex=0, yAxisIndex=0, **kwargs):
        config = {
            'lineStyle': {
                'normal': {
                    'color': color,
                    'width': linewidth,
                    'opacity': opacity,
                }
            },
            'itemStyle': {
                'normal': {
                    'color': color,
                }
            },

            'smooth': smooth,
        }

        if fill:
            config['areaStyle'] = {
                'normal': {
                    'color': color,
                    'opacity': opacity,
                }
            }
            kwargs.setdefault('areaStyle', config['areaStyle'])

        kwargs.setdefault('lineStyle', config['lineStyle'])
        kwargs.setdefault('itemStyle', config['itemStyle'])
        kwargs.setdefault('smooth', config['smooth'])
        self._add(label, type='line', data=data, xAxisIndex=xAxisIndex, legend=legend,
                  yAxisIndex=yAxisIndex, **kwargs)

    def kline(self, label, data, upcolor='#52b986', downcolor='#ec4d5c', opacity=1, legend=True, xAxisIndex=0,
              yAxisIndex=0,
              **kwargs):
        config = {
            'itemStyle': {
                'normal': {
                    'color': upcolor,
                    'color0': downcolor,
                    'borderColor': None,
                    'borderColor0': None,
                    'opacity': opacity,
                }
            }
        }
        kwargs.setdefault('itemStyle', config['itemStyle'])
        self._add(label, type='candlestick', data=data, xAxisIndex=xAxisIndex, legend=legend,
                  yAxisIndex=yAxisIndex, **kwargs)

    def bar(self, label, data, color='#91c7af', opacity=1, xAxisIndex=0, yAxisIndex=0, legend=True, **kwargs):
        config = {
            'itemStyle': {
                'normal': {
                    'color': color,
                    'opacity': opacity,
                }
            }
        }
        kwargs.setdefault('itemStyle', config['itemStyle'])
        self._add(label, type='bar', data=data, xAxisIndex=xAxisIndex,
                  yAxisIndex=yAxisIndex, legend=legend, **kwargs)

    def _add(self, name=None, type=None, data=None, xAxisIndex=0,
             yAxisIndex=0, legend=True, **kwargs):
        if legend:
            self.legend['data'].append(name)
        series = {
            'name': name,
            'type': type,
            'data': data,
            'xAxisIndex': xAxisIndex,
            'yAxisIndex': yAxisIndex,
        }
        if kwargs:
            series.update(kwargs)
        self.series.append(series)

    @property
    def json(self):
        config = {
            'series': self.series,
            'legend': self.legend,
            'tooltip': self.tooltip,
            'yAxis': self.y_axis if self.y_axis else [{}],
            'xAxis': self.x_axis if self.x_axis else [{}],
        }
        if not self._show_x_axis:
            config['xAxis'] = {'show': False}
        if not self._show_y_axis:
            config['yAxis'] = {'show': False}
        if not self._show_legend:
            config['legend'] = {'show': False}

        self._option.update(config)
        return self._option

    def _check_title(self, title):
        if title is None:
            return []
        elif isinstance(title, list):
            return list(map(dict, title))
        return [title.json]


class Page(RenderMixin):
    """单页面多图"""

    def __init__(self):
        self.charts = []

    def add(self, chart_or_charts):
        if isinstance(chart_or_charts, list):
            self.charts += chart_or_charts
        else:
            self.charts.append(chart_or_charts)

    def _render_content(self):
        chart_content = b''
        for chart in self.charts:
            chart_content += chart._render_content()
            chart_content += b'<br>'
        return chart_content
