#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/12/8 15:04
@annotation = ''
"""
import datetime
import json
import os


# from ..echart_util.chart import Chart, Page
# from ..echart_util.component import Text, Axis
#
# __all__ = [
#     'Text',
#     'Axis',
#     'Chart',
#     'Page',
# ]
class JSONEncodeHelper(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            try:
                return obj.astype(float).tolist()
            except:
                try:
                    return obj.astype(str).tolist()
                except:
                    return json.JSONEncoder.default(self, obj)


def json_dumps(data, indent=0):
    return json.dumps(data, indent=indent, cls=JSONEncodeHelper)


def get_resource(html_name):
    return os.path.join(os.path.dirname(__file__), 'templates', html_name + '.html')


def get_chart_id():
    import uuid
    return uuid.uuid4().hex


class RenderMixin(object):
    def _render(self):
        content = self._render_content()
        with open(get_resource('temp'), 'rb') as f:
            temp = f.read()
            temp = temp.replace(b'{{ content }}', content)
        return temp

    def plot(self):
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(suffix='.html', ) as fobj:
            fobj.write(self._render())
            fobj.flush()
            webbrowser.open('file://' + os.path.realpath(fobj.name))
            input('Press enter for continue')

    def save(self, path, file_name):
        if not os.path.exists(path):
            os.mkdir(path)
        with open(os.path.join(path, str(file_name) + '.html'), 'wb') as f:
            f.write(self._render())
