#!/usr/bin/env python3

import os
import sys
import argparse

VPLOTLIB_FOLDER = '/mnt/c/Users/visesha/Work/Tools/vplotlib'

from ptypes import ptypes

parser = argparse.ArgumentParser()

parser.add_argument('--type', required=True, action='store')
parser.add_argument('--file', required=True, action='store')
parser.add_argument('--output', action='store', default=None)

parser.add_argument('--title', action='store', default=None)
parser.add_argument('--xlabel', action='store', default=None)
parser.add_argument('--ylabel', action='store', default=None)

parser.add_argument('--ymin', action='store', type=float, default=None)
parser.add_argument('--ymax', action='store', type=float, default=None)
parser.add_argument('--ystep', action='store', type=float, default=None)
parser.add_argument('--opt-tics', action='store', type=int, default=10)
parser.add_argument('--ypercent', action='store_true', default=False)

parser.add_argument('--xmin', action='store', type=float, default=None)
parser.add_argument('--xmax', action='store', type=float, default=None)

parser.add_argument('--override-file', action='append', default=[])
parser.add_argument('--overrides', action='store', nargs='*', default=[])

parser.add_argument('--open', action='store_true', default=False)

args = parser.parse_args()

# club all overrides
override_list = []
overrides = dict()

for override_file in args.override_file:
    with open('override_file') as f:
        override_list += f.read().split('\n')
override_list += args.overrides

for override in override_list:
    field, value = override.split('=') if override.count('=') == 1\
        else override.split('==')
    overrides[field] = eval(value)

# get the template
(plot_class, plot_template) = ptypes[args.type]

# apply overrides
for field, value in overrides.items():
    group, key = field.split(':')
    if group not in plot_template:
        raise RuntimeError("Invalid group `%s' in template" % group)
    if key not in plot_template[group]:
        raise RuntimeError("Invalid key in `%s' in template[%s]" % (key, group)) 
    plot_template[group][key] = value

plt = plot_class()
plt.title = args.title
plt.ylabel = args.ylabel
plt.xlabel = args.xlabel
plt.ymax = args.ymax
plt.ymin = args.ymin
plt.ystep = args.ystep
plt.opt_tics = args.opt_tics
plt.ypercent = args.ypercent

plt.xmax = args.xmax
plt.xmin = args.xmin



with open(args.file) as f:
    plt.load_data(f.read())

output = args.file if args.output is None else args.output
if output.endswith('.csv'):
    output = output[:-4]

print ('Generating TeX file ... ', end='')
with open('%s.tex' % output, 'w') as f:
    f.write(plt.plot(plot_template).render())
print ('Done')
os.system('%s/compile.py %s.tex' % (VPLOTLIB_FOLDER, output))

print ('Output written to %s.pdf' % output)

if args.open:
    os.system('evince %s.pdf > /dev/null 2>&1' % output)
