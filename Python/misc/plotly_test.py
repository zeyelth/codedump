# -*- coding: utf-8 -*-
'''
Copyright (c) 2018 Victor Wåhlström

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import plotly.offline
import plotly.graph_objs

source_data = {
    'FreehandStrokeBenchmark::testDefaultTip(): Blocking': [4065, 2319, 1736, 1627, 1496, 1481, 1412, 1410, 1343, 1306, 1506, 1593, 1648, 1572, 1610, 1653, 1786, 1570, 1958, 1596],
    'FreehandStrokeBenchmark::testDefaultTip(): Lock free': [4265, 2225, 1698, 1456, 1237, 1157, 1091, 1117, 1029, 988, 1011, 977, 918, 961, 955, 1002, 1033, 1078, 1014, 990],
    'FreehandStrokeBenchmark::testDefaultTip(): Locks fixed + lock free': [4133, 2166, 1633, 1332, 1083, 1009, 947, 906, 891, 835, 893, 837, 862, 863, 845, 833, 872, 890, 865, 898],
}


def _build_graph(name, data):
    return plotly.graph_objs.Scatter(
        x=list(range(1, len(data) + 1)),
        y=data,
        name=name)


if __name__ == '__main__':
    data = [_build_graph(k, v) for k, v in source_data.items()]

    layout = {'title': 'Krita benchmark tests',
              'xaxis': {'title': 'Threads',
                        'dtick': 1},
              'yaxis': {'title': 'Milliseconds'}}

    fig = {'data': data, 'layout': layout}

    plotly.offline.plot(fig, filename='krita_benchmark_plot.html', show_link=False)
