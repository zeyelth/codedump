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


class CirDataException(Exception):
    pass


class Cir(DataParser):
    def __init__(self):
        super(Cir, self).__init__()

    def normalize_data(self):
        materials = self.data['materials']
        self.data['material_count'] = len(materials)

        for material in materials:
            material['name_length'] = len(material['name'])
            material['texture_name_length'] = len(material['texture_name'])

        self.data['unknown_count'] = len(self.data['unknowns'])

        joints = self.data['joints']
        self.data['joint_count'] = len(joints)

        for joint in joints:
            joint['name_length'] = len(joint['name'])
            joint['child_count'] = len(joint['children'])

        mesh_groups = self.data['mesh_groups']
        self.data['mesh_group_count'] = len(mesh_groups)

        for mesh_group in mesh_groups:
            mesh_group['name_length'] = len(mesh_group['name'])

            faces = mesh_group['faces']
            mesh_group['face_count'] = len(faces)

            for face in faces:
                face['vertex_count'] = len(face['vertices'])
                face['triangle_count'] = len(face['triangles'])

            mesh_group['unknown1_count'] = len(mesh_group['unknowns1'])
            mesh_group['unknown2_count'] = len(mesh_group['unknowns2'])

    def load_data(self, data):
        self.clear()

        i = 0
        identifier, version = struct.unpack('<2I', data[i:i + 8])
        i += 8

        self.data['id'] = identifier
        self.data['version'] = version

        if identifier != 4:
            raise CirDataException("Unknown file ID: {0}".format(identifier))

        if version == 16:
            unused, unknown2, material_count = struct.unpack('<IfI', data[i:i + 12])
            i += 12
            self.data['unused'] = unused
            self.data['unknown2'] = unknown2
            self.data['material_count'] = material_count
        elif version == 256:
            unknown1, unused, unknown2, material_count = struct.unpack('<2IfI', data[i:i + 16])
            i += 16
            self.data['unknown1'] = unknown1
            self.data['unused'] = unused
            self.data['unknown2'] = unknown2
            self.data['material_count'] = material_count
        else:
            raise CirDataException("Unknown file version: {0}".format(version))

        materials = []
        for _ in range(material_count):
            material = OrderedDict()

            name_length, = struct.unpack('<I', data[i:i + 4])
            i += 4

            name, = struct.unpack('<{0}s'.format(name_length), data[i:i + name_length])
            i += name_length

            unknown, texture_name_length, = struct.unpack('<2I', data[i:i + 8])
            i += 8

            texture_name, = struct.unpack('<{0}s'.format(texture_name_length), data[i:i + texture_name_length])
            i += texture_name_length

            r, g, b = struct.unpack('<3f', data[i:i + 12])
            i += 12

            material['name_length'] = name_length
            material['name'] = name
            material['unknown'] = unknown
            material['texture_name_length'] = texture_name_length
            material['texture_name'] = texture_name

            color = OrderedDict()
            color['r'] = r
            color['g'] = g
            color['b'] = b

            material['color'] = color

            materials.append(material)

        self.data['materials'] = materials

        unknown_count, = struct.unpack('<I', data[i:i + 4])
        i += 4

        self.data['unknown_count'] = unknown_count

        unknowns = []
        for _ in range(unknown_count):
            unknown = OrderedDict()
            unknown1, unknown2, unknown3, unknown4 = struct.unpack('<4f', data[i:i + 16])
            i += 16

            unknown['unknown1'] = unknown1
            unknown['unknown2'] = unknown2
            unknown['unknown3'] = unknown3
            unknown['unknown4'] = unknown4
            unknowns.append(unknown)
        self.data['unknowns'] = unknowns

        joint_count, = struct.unpack('<I', data[i:i + 4])
        i += 4

        self.data['joint_count'] = joint_count

        joints = []
        for _ in range(joint_count):
            name_length, = struct.unpack('<I', data[i:i + 4])
            i += 4

            name, = struct.unpack('<{0}s'.format(name_length), data[i:i + name_length])
            i += name_length

            unknown, child_count = struct.unpack('<fI', data[i:i + 8])
            i += 8

            children = list(struct.unpack('<{0}I'.format(child_count), data[i:i + child_count * 4]))
            i += child_count * 4

            joint = OrderedDict()
            joint['name_length'] = name_length
            joint['name'] = name
            joint['unknown'] = unknown
            joint['child_count'] = child_count
            joint['children'] = children

            joints.append(joint)

        self.data['joints'] = joints

        mesh_group_count, = struct.unpack('<I', data[i:i + 4])
        i += 4

        self.data['mesh_group_count'] = mesh_group_count

        mesh_groups = []
        for _ in range(mesh_group_count):
            name_length, = struct.unpack('<I', data[i:i + 4])
            i += 4

            name, = struct.unpack('<{0}s'.format(name_length), data[i:i + name_length])
            i += name_length

            face_count, = struct.unpack('<I', data[i:i + 4])
            i += 4

            mesh_group = OrderedDict()
            mesh_group['name_length'] = name_length
            mesh_group['name'] = name
            mesh_group['face_count'] = face_count

            faces = []
            for _ in range(face_count):
                material_index, vertex_count = struct.unpack('<2I', data[i:i + 8])
                i += 8

                face = OrderedDict()
                face['material_index'] = material_index
                face['vertex_count'] = vertex_count

                vertices = []
                for _ in range(vertex_count):
                    x1, y1, z1, x2, y2, z2, nx, ny, nz, u, v, joint1, joint2, weight = struct.unpack('<11f2If', data[i:i + 56])
                    i += 56

                    vertex = OrderedDict()
                    position_joint1 = OrderedDict()
                    position_joint1['x'] = x1
                    position_joint1['y'] = y1
                    position_joint1['z'] = z1
                    vertex['position_joint1'] = position_joint1

                    position_joint2 = OrderedDict()
                    position_joint2['x'] = x2
                    position_joint2['y'] = y2
                    position_joint2['z'] = z2
                    vertex['position_joint2'] = position_joint2

                    normal = OrderedDict()
                    normal['x'] = nx
                    normal['y'] = ny
                    normal['z'] = nz
                    vertex['normal'] = normal

                    uv = OrderedDict()
                    uv['u'] = u
                    uv['v'] = v
                    vertex['uv'] = uv

                    vertex['joint1'] = joint1
                    vertex['joint2'] = joint2
                    vertex['weight'] = weight

                    vertices.append(vertex)

                face['vertices'] = vertices

                triangle_count, = struct.unpack('<I', data[i:i + 4])
                i += 4

                face['triangle_count'] = triangle_count

                triangles = []
                for _ in range(triangle_count):
                    v1, v2, v3 = struct.unpack('<3I', data[i:i + 12])
                    i += 12
                    triangle = [v1, v2, v3]
                    triangles.append(triangle)
                face['triangles'] = triangles

                faces.append(face)

            mesh_group['faces'] = faces

            unknown1_count, = struct.unpack('<I', data[i:i + 4])
            i += 4

            mesh_group['unknown1_count'] = unknown1_count

            unknowns1 = []
            for _ in range(unknown1_count):
                unknown1, unknown2, unknown3, unknown4, unknown5 = struct.unpack('<4fI', data[i:i + 20])
                i += 20

                unknown = OrderedDict()
                unknown['unknown1'] = unknown1
                unknown['unknown2'] = unknown2
                unknown['unknown3'] = unknown3
                unknown['unknown4'] = unknown4
                unknown['unknown5'] = unknown5
                unknowns1.append(unknown)

            mesh_group['unknowns1'] = unknowns1

            unknown2_count, = struct.unpack('<I', data[i:i + 4])
            i += 4

            mesh_group['unknown2_count'] = unknown2_count

            unknowns2 = []
            for _ in range(unknown2_count):
                name_length = struct.unpack('<I', data[i:i + 4])
                i += 4

                name = struct.unpack('<{0}s'.format(name_length), data[i:i + name_length])
                i += name_length

                unknown1, unknown2, unknown3, unknown4, unknown5, unknown6, unknown7, unknown8, unknown9 = struct.unpack('<8fI', data[i:i + 36])
                i += 36

                unknown = OrderedDict()

                unknown['name_length'] = name_length
                unknown['name'] = name
                unknown['unknown1'] = unknown1
                unknown['unknown2'] = unknown2
                unknown['unknown3'] = unknown3
                unknown['unknown4'] = unknown4
                unknown['unknown5'] = unknown5
                unknown['unknown6'] = unknown6
                unknown['unknown7'] = unknown7
                unknown['unknown8'] = unknown8
                unknown['unknown9'] = unknown9

                unknowns2.append(unknown)

            mesh_group['unknowns2'] = unknowns2
            mesh_groups.append(mesh_group)

        self.data['mesh_groups'] = mesh_groups
