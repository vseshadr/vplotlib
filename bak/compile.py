#!/usr/bin/env python3

import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--open', action='store_true', default=False)
parser.add_argument('file')
args = parser.parse_args()

VPLOTLIB_FOLDER = 'VPLOTLIB_FOLDER_PATH'

filename = args.file[:-4]

os.system('cp %s.tex %s/compile/picture.tex' % (filename, VPLOTLIB_FOLDER))
print ('Compiling the PDF file ... ', end='')
os.system('pdflatex -halt-on-error %s/compile/wrapper.tex > /dev/null' % VPLOTLIB_FOLDER)
print ('Done')
print ('Cropping PDF ... ', end='')
os.system('pdfcrop --noverbose wrapper.pdf %s.pdf > /dev/null' % (filename))
print ('Done')
print ('Cleaning up ... ', end='')
os.system('rm -f wrapper.*')
print ('Done')

if args.open:
    os.system('evince %s.pdf > /dev/null 2>&1' % filename)
