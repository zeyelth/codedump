# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Victor Wåhlström

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


# Quick and dirty hack to extract json data from KDE projects' bug overview pages.
# This code will be obsolete if or when REST API support is added to the bug tracker.

# NOTE: This is proof of concept code parsing html, and will most likely break if the layout ever changes!

# Requires Python 3.0 or above

# Usage: python kde_bugtracker_parser.py "project name"


from html.parser import HTMLParser
import json
import sys
import urllib.request


class KDEBugReportParser(HTMLParser):
    
    def __init__(self):
        super(KDEBugReportParser, self).__init__()
        self._table_data = {}
        self._inside_table = False
        self._inside_tr = False
        self._inside_td = False
        self._data = []

        self._components = {}
        self._link_prefix = ''

    def to_dict(self):
        return self._components

    def set_link_prefix(self, prefix):
        self._link_prefix = prefix

    def _process_string(self, string):
        return string.replace("\\'", "'")

    def _post_process(self):
        self._components = {}
        for d in self._data[1:]:
            component = {}
            name = d[0][0]
            bugs = {}
            component['bugs'] = bugs
            for i, b in enumerate(d[1:]):
                severity = self._data[0][i + 1][0]
                assert severity not in bugs
                bugs[severity] = {'count': int(b[0]),
                                  'link': self._link_prefix + b[1]}
            assert name not in self._components
            self._components[name] = component

    def feed(self, data):
        super(KDEBugReportParser, self).feed(data)
        self._post_process()

    def handle_starttag(self, tag, attrs):
        if self._inside_table and tag == 'tr':
            self._data.append([])
            self._inside_tr = True
        elif self._inside_tr and tag == 'td':
            self._data[-1].append([0, ''])
            self._inside_td = True
        elif tag == 'table':
            # assume that the page contains only one table, and that this contains the data we are after
            self._inside_table = True

        if self._inside_td:
            assert self._inside_table and self._inside_tr
            # assume links are bug links
            if tag == 'a' and len(attrs) > 0 and attrs[0][0] == 'href':
                self._data[-1][-1][1] = self._process_string(attrs[0][1])

    def handle_endtag(self, tag):
        if not self._inside_table:
            return
        if tag == 'tr':
            self._inside_tr = False
        elif tag == 'td':
            self._inside_td = False
        elif tag == 'table':
            self._inside_table = False
    def handle_data(self, data):
        if self._inside_td:
            assert self._inside_table and self._inside_tr
            data = self._process_string(data)
            self._data[-1][-1][0] = data


def get_data(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')


if __name__ == '__main__':
    if sys.version_info[0] != 3:
        sys.exit(1)

    if len(sys.argv) < 2:
        sys.exit(1)

    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_- "

    product = ''.join([c for c in sys.argv[1] if c in allowed_chars])

    data = get_data('https://bugs.kde.org/component-report.cgi?product={}'.format(product))

    parser = KDEBugReportParser()
    parser.set_link_prefix('https://bugs.kde.org/')
    parser.feed(data)

    print(json.dumps(parser.to_dict(), sort_keys=True, indent=4))
