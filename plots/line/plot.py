"""Line plot"""

from plots.base.plot import Plot

from tikz.latex import LatexLength as latex_length
from tikz.latex import LatexDef as latex_def
from tikz.latex import LatexText as latex_text
from tikz.comment import TikZComment as tikz_comment
from tikz.style import TikZStyle as tikz_style
from tikz.shapes import TikZRectangle as tikz_rectangle
from tikz.shapes import TikZPath as tikz_path
from tikz.node import TikZNode as tikz_node

class LinePlot(Plot):

    def __init__(self):

        Plot.__init__(self)

        self._legends = None
        self._line_data = None
        self._xkeys = None

        self._has_ytics = True
        self._ycontinuous = True
        self._auto_ytics = True

        self._has_xtics = True
        self._xcontinuous = False
        self._xtics_all = True
        self._auto_xtics = False

        self._has_legend = True
        self._legend_type = 'line'

        self._line_ns = ['lone', 'ltwo', 'lthree', 'lfour', 'lfive',
                        'lsix', 'lseven', 'leight', 'lnine', 'lten']
       

    def load_data(self, string):
        lines = string.split('\n')
        legends = lines[0].split(',')[1:]
        line_data = []
        xkeys = []

        for i in legends:
            line_data.append([])

        for line in lines[1:]:
            if len(line.strip()):
                fields = line.split(',')
                key = fields[0]
                xkeys.append(key)
                values = [float(field) for field in fields[1:]]
                for j, value in enumerate(values):
                    line_data[j].append(value)

        self._xkeys = xkeys
        self._legends = legends
        self._line_data = line_data

    def _get_ymax(self):
        return max(max(line) for line in self._line_data)

    def _get_ymin(self):
        return min(min(line) for line in self._line_data)

    def _get_plot_area(self, template):
        num_keys = len(self._xkeys)+2
        num_legs = len(self._legends)
        assert(num_keys > 1)
        xstep_frac = 1.0 / (num_keys - 1)
        xstep_def = latex_length('xstep', '%f\\xmax' % xstep_frac)
        self._definitions.append(xstep_def)
        
        style_key = 'line-styles-%d' % num_legs
        if style_key in template['line']:
            line_styles = template['line'][style_key]
        else:
            line_styles = template['line']['line-styles-n'][:num_legs]

        line_style_comment = tikz_comment('line styles')
        line_style_comment.space_before = 1
        self._definitions.append(line_style_comment)
        for i, style in enumerate(line_styles):
            line_style_name = self._line_ns[i]
            line_style = tikz_style(line_style_name)
            line_style.set_option(style)
            self._definitions.append(line_style)

        # plot the lines
        line_comment = tikz_comment('Lines')
        line_comment.space_before = 1
        self._plot_elements.append(line_comment)

        base = '0' if self.ymin <= 0 else '\\ymin'
        baseline_def = latex_def('base', base)
        self._plot_elements.append(baseline_def)
        for i, values in enumerate(self._line_data):
            points = []
            for j, value in enumerate(values):
                points.append('(%d\\xstep, %s)' % (j+1, value))
            path = tikz_path(points)
            path.set_option(self._line_ns[i])
            path.set_option('rounded corners', '0.1pt')
            self._plot_elements.append(path)

        # plot markers
        if template['marker']['display']:
            marker_styles = template['marker']['marker-styles']
            for i, values in enumerate(self._line_data):
                for j, value in enumerate(values):
                    marker_node = tikz_node()
                    marker_node.location = '(%d\\xstep, %s)' % (j+1, value) 
                    marker_node.set_option('mark size', '1pt')
                    marker_node.set_option('anchor', 'center')
                    #marker_node.set_option('xshift', '-1.5pt')
                    marker_node.content = latex_text('\\pgfuseplotmark{%s}' % (marker_styles[i]))
                    self._plot_elements.append(marker_node)

                
    def _get_xtics(self):
        xtics = []
        for i, key in enumerate(self._xkeys):
            loc = '%f\\xstep' % (i+1)
            xtics.append((loc, key))
        return xtics

    def _get_legends(self):
        legends = []
        for i, legend in enumerate(self._legends):
            style = self._line_ns[i]
            legends.append((style, legend))
        return legends
