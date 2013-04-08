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
from dataparser import DataParser


class AniDataException(Exception):
    pass


class Ani(DataParser):
    def __init__(self):
        super(Ani, self).__init__()

    def normalize_data(self):
        joints = self.data['joints']
        self.data['joint_count'] = len(joints)
        for joint in joints:
            keys = joint['keys']
            joint['key_count'] = len(keys)

    def load_data(self, data):
        self.clear()

        i = 0
        identifier, version = struct.unpack('<2I', data[i:i + 8])
        i += 8

        if identifier != 3:
            raise AniDataException("Unknown file ID: {0}".format(identifier))

        self.data['id'] = identifier
        self.data['version'] = version

        if version == 3:
            animation_length, unused, joint_count = struct.unpack('<3I', data[i:i + 12])
            i += 12
            if unused != 0xdeadbabe:
                raise AniDataException("Unexpected data encountered")

            self.data['animation_length'] = animation_length
            self.data['unused'] = unused
            self.data['joint_count'] = joint_count
        elif version == 256:
            unknown, unused, animation_length, joint_count = struct.unpack('<4I', data[i:i + 16])
            i += 16
            if unknown != 0xa9f5d5ce or unused != 0xdeadbabe:
                raise AniDataException("Unexpected data encountered")

            self.data['unknown'] = unknown
            self.data['unused'] = unused
            self.data['animation_length'] = animation_length
            self.data['joint_count'] = joint_count
        else:
            raise AniDataException("Unknown file version: {0}".format(version))

        joints = []
        for _ in range(joint_count):
            index, key_count = struct.unpack('<2I', data[i:i + 8])
            i += 8
            keys = []
            joint = OrderedDict()
            joint['index'] = index
            joint['key_count'] = key_count
            for _ in range(key_count):
                time, qx, qy, qz, qw, px, py, pz = struct.unpack('<I7f', data[i:i + 32])
                i += 32

                quaternion = OrderedDict()
                quaternion['x'] = qx
                quaternion['y'] = qy
                quaternion['z'] = qz
                quaternion['w'] = qw

                position = OrderedDict()
                position['x'] = px
                position['y'] = py
                position['z'] = pz

                key = OrderedDict()
                key['time'] = time
                key['qrotation'] = quaternion
                key['position'] = position
                keys.append(key)
            joint['keys'] = keys
            joints.append(joint)
        self.data['joints'] = joints
