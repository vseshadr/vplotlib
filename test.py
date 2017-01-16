import os

from plots.base.plot import Plot
from plots.base.template import template as base_template

from plots.cstack.plot import ColumnStackPlot
from plots.cstack.template import template as cstack_template

plt = ColumnStackPlot()
plt.title = 'Test plot'
plt.xlabel = 'Test xlabel'
plt.ylabel = 'Test ylabel'
plt.ymax = 17
plt.ymin = 0

cstack_template['xtics']['rotate'] = 90
cstack_template['cstack']['padding'] = 1

with open('examples/prefetch-lifetime') as f:
    plt.load_data(f.read())


with open('a.tex', 'w') as f:
    f.write(plt.plot(cstack_template).render())

os.system('cp a.tex compile/picture.tex')
os.system('pdflatex -halt-on-error compile/wrapper.tex > /dev/null')
os.system('pdfcrop wrapper.pdf a.pdf > /dev/null')
os.system('rm -f wrapper.*')
