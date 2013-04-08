# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 Victor Wåhlström

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
'''

from collections import OrderedDict
import json
import struct
import os


class DataParserException(Exception):
    pass


class DataParser(object):

    def __init__(self):
        self.clear()

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def load_data(self, data):
        """
        Loads raw data
        """
        raise DataParserException("Not implemented!")

    def normalize_data(self):
        """
        Recalculates redundantly stored data such as string lengths and sizes
        """
        raise DataParserException('Not implemented!')

    def clear(self):
        self.data = OrderedDict()

    def load(self, data):
        """
        Loads data
        :param data: Data to load, can be a file path, raw data, or a string on the same format as returned by __str__
        """

        try:
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    raw_data = f.read()
                    self.load_data(raw_data)
                    return
        except TypeError:
            # not a file path
            pass

        try:
            self.data = json.loads(data, object_pairs_hook=OrderedDict)
            self.normalize_data()
            return
        except ValueError:
            # not a string representation, raw data?
            pass

        self.load_data(data)

    def pack(self):
        """
        Returns a binary representation of the data
        """
        fmt = ["<"]
        datalist = []

        def _pack_item(item):
            if isinstance(item, int):
                datalist.append(item)
                fmt.append("I")  # assume int is uint32
            elif isinstance(item, float):
                datalist.append(item)
                fmt.append("f")
            elif isinstance(item, (str, unicode)):  # manipulating data can change it to unicode...
                datalist.append(item.encode("iso-8859-1"))
                fmt.append("{0}s".format(len(item)))
            elif isinstance(item, list):
                for v in item:
                    _pack_item(v)
            elif isinstance(item, OrderedDict):
                for v in item.itervalues():
                    _pack_item(v)
            else:
                raise DataParserException("Encountered unknown type '{0}' while packing item: {1}".format(type(item), item))

        for v in self.data.itervalues():
            _pack_item(v)

        return struct.pack("".join(fmt), *datalist)
