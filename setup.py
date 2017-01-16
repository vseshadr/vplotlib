#!/usr/bin/env python

import os

file_map = {
    'vplot.py' : 'vplot.py',
    'debug-vplot' : 'debug-vplot',
    'compile.py' : 'compile.py',
    'wrapper.tex' : 'compile/wrapper.tex'
}

cwd = os.getcwd()

for src, dst in file_map.items():
    with open('bak/%s' % (src)) as f:
        file_data = f.read()
    with open(dst, 'w') as f:
        f.write(file_data.replace('VPLOTLIB_FOLDER_PATH', cwd))
