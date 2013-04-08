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

import struct
from collections import OrderedDict


class XarcDataException(Exception):
    pass


class Xarc(object):
    def __init__(self):
        self.unknown = 1
        self._files = OrderedDict()

    def load(self, filename):
        """
        Loads a .xarc file into memory
        :param filename: the path to a .xarc file
        """

        with open(filename, 'rb') as f:
            data = f.read()

        self.unknown, num_files, base_offset = struct.unpack('<3I', data[0:12])
        if self.unknown != 1:
            raise XarcDataException("First uint32 in file '{0}' was {1}, expected 1".format(filename, self.unknown))
        i = 12
        file_descs = OrderedDict()  # order is important señorita...

        self._files = OrderedDict()

        if base_offset == i:  # no files
            return

        def _get_file_desc(data, offset):
            name = ""
            i = offset
            c = data[i]
            i += 1
            while c != '\0':
                name += c
                c = data[i]
                i += 1

            size, unknown = struct.unpack('<2I', data[i:i + 8])
            i += 8

            if unknown != 0:  # TODO: seems to always be zero, investigate if not
                raise XarcDataException("Found non-zero unknown data for file '{0}': {1}".format(name, unknown))
            return i - offset, name, size

        while i < base_offset:
            file_desc = _get_file_desc(data, i)
            file_descs[file_desc[1]] = file_desc[2]
            i += file_desc[0]

        for name, size in file_descs.iteritems():
            self._files[name] = data[i:i + size]
            i += size

        if num_files != len(self._files):
            raise XarcDataException("Archive reported {0} files, found {1} files".format(num_files, len(self._files)))

    def get_file_names(self):
        if self._files is None:
            return []

        return self._files.keys()

    def get_data(self, filename):
        return self._files.get(filename, None)

    def insert_data(self, filename, data):
        self._files[filename] = data

    def pack(self):
        filedata = ""
        descdata = ""
        for k, v in self._files.iteritems():
            name = k + "\0"
            descdata += struct.pack('<{0}s2I'.format(len(name)), name, len(v), 0)  # 0 is the unknown data in a file description
            filedata += v

        base_offset = 12 + len(descdata)

        data = struct.pack('<3I', self.unknown, len(self._files), base_offset) + descdata + filedata
        return data
