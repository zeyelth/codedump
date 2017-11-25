# -*- coding: utf-8 -*-
'''
Copyright (c) 2017 Victor Wåhlström

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


import sys
import argparse

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        sys.exit("This script requires Python 3 or up!")

    parser = argparse.ArgumentParser(description='Normalize and convert newline characters between CRLF and LF in text files')
    parser.add_argument('-i', dest='input', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file path. If unspecified, stdin will be used')
    parser.add_argument('-o', dest='output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Output file path. If unspecified, stdout will be used')
    parser.add_argument('--control-characters', dest='delim', choices=['LF', 'CRLF'], default='LF', help='Control character sequence that denote line endings in the output file. If unspecified, LF (Line Feed) will be used.')

    args = parser.parse_args()

    if args.delim == 'LF':
        delim = '\n'
    elif args.delim == 'CRLF':
        delim = '\r\n'
    else:
        sys.exit('Unknown control character sequence!')

    lines = args.input.read().splitlines()
    args.output.write(delim.join(lines))
