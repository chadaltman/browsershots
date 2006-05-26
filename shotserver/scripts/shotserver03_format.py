#! /usr/bin/python
# -*- coding: utf-8 -*-
# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Check formatting of Python source code.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import sys

class FormatError:
    def __init__(self, filename, lineno, error):
        self.message = "%s:%d: %s" % (filename, lineno, error)

def read_blocks(filename):
    blocks = []
    block = []
    start = 1
    docstring = False
    lines = file(filename).readlines()
    if not lines[-1].endswith('\n'):
        raise FormatError(filename, len(lines), 'no newline before EOF')
    lines.append('')
    for number, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '"""' and not docstring:
            stripped = ''
            docstring = True
        if stripped or docstring:
            block.append(line)
        else:
            if block:
                blocks.append([start, block])
                if len(blocks) > 4:
                    break
                block = []
            start = number + 2
        if stripped == '"""' and docstring:
            docstring = False
    return blocks

def remove_shebang(head):
    if head[1][0] == '#! /usr/bin/python\n':
        head[0] += 1
        head[1].pop(0)

def check_file(filename):
    blocks = read_blocks(filename)
    head, docstring, keywords = blocks[:3]
    remove_shebang(head)
    if head[1] != ref_head[1]:
        for offset, line in enumerate(head[1]):
            if offset >= len(ref_head[1]):
                raise FormatError(filename, head[0] + offset, "copyright too short")
            if line != ref_head[1][offset]:
                raise FormatError(filename, head[0] + offset, "wrong copyright")
        raise FormatError(filename, head[0] + len(head[1]), "copyright too short")
    if docstring[1][0].strip() != '"""':
        raise FormatError(filename, docstring[0], "missing docstring")
    if docstring[1][-1].strip() != '"""':
        raise FormatError(filename, docstring[0] + len(docstring[1]) - 1, "missing docstring")
    if len(docstring[1]) < 3:
        raise FormatError(filename, docstring[0] + 1, "empty docstring")
    if not keywords[1][0].startswith("__revision__ = '$Rev:"):
        raise FormatError(filename, keywords[0], "missing __revision__ = '$Rev:")
    if not keywords[1][1].startswith("__date__ = '$Date:"):
        raise FormatError(filename, keywords[0] + 1, "missing __date__ = '$Date:")
    if not keywords[1][2].startswith("__author__ = '$Author:"):
        raise FormatError(filename, keywords[0] + 2, "missing __author__ = '$Author:")

reference = read_blocks(sys.argv[0])
ref_head, ref_docstring, ref_keywords = reference[:3]
remove_shebang(ref_head)

error = False
files = sys.argv[1:]
files.sort()
for filename in files:
    try:
        check_file(filename)
    except FormatError:
        error = True
if error:
    sys.exit(error)
