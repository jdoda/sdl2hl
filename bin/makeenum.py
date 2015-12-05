#!/bin/env python

import sys

from sdl2._sdl2 import lib


def make_enum(enum_name, defn_prefix):
    enum_src = 'class %s(IntEnum):\n' % enum_name

    for name in dir(lib):
        if name.startswith(defn_prefix):
            enum_src += '    %s = lib.%s\n' % (name[len(defn_prefix):].lower(), name)
    return enum_src


if __name__ == '__main__':
    print make_enum(sys.argv[1], sys.argv[2])
