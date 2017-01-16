"""This file lists all the available plot types."""

from plots.base.plot import Plot
from plots.base.template import template as base_template

from plots.cstack.plot import ColumnStackPlot
from plots.cstack.template import template as cstack_template

from plots.rstack.plot import RowStackPlot
from plots.rstack.template import template as rstack_template

from plots.line.plot import LinePlot
from plots.line.template import template as line_template



ptypes = {
    'cstack' : (ColumnStackPlot, cstack_template),
    'rstack' : (RowStackPlot, rstack_template),
    'line' : (LinePlot, line_template),
}
