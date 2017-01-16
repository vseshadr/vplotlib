"""Row stack bar plot"""

from plots.base.plot import Plot

from tikz.latex import LatexLength as latex_length
from tikz.latex import LatexDef as latex_def
from tikz.comment import TikZComment as tikz_comment
from tikz.style import TikZStyle as tikz_style
from tikz.shapes import TikZRectangle as tikz_rectangle

class RowStackPlot(Plot):

    def __init__(self):

        Plot.__init__(self)

        self._column_headers = None
        self._clusters = None

        self._has_ytics = True
        self._ycontinuous = True
        self._auto_ytics = True

        self._has_xtics = True
        self._xcontinuous = False
        self._xtics_all = True
        self._auto_xtics = False

        self._has_legend = True
        self._legend_type = 'box'

        self._bar_ns = ['bone', 'btwo', 'bthree', 'bfour', 'bfive',
                        'bsix', 'bseven', 'beight', 'bnine', 'bten']
       

    def load_data(self, string):
        lines = string.split('\n')
        column_header = lines[0].split(',')[1:]
        clusters = []

        for line in lines[1:]:
            if len(line.strip()):
                fields = line.split(',')
                key = fields[0]
                values = [float(field) for field in fields[1:]]
                clusters.append((key, values))

        self._column_header = column_header
        self._clusters = clusters


    def _get_ymax(self):
        return max(sum(cluster[1]) for cluster in self._clusters)

    def _get_ymin(self):
        return 0

    def _get_plot_area(self, template):

        plot_area_elements = []
        
        num_bars_cluster = len(self._column_header)
        num_clusters = len(self._clusters)
        cluster_padding = template['rstack']['padding']
        cluster_width_bars = 1 + 2*cluster_padding

        total_bar_count = cluster_width_bars * num_clusters
        bar_frac = 1.0 / total_bar_count

        bar_width_def = latex_length('barwidth', '%f\\xmax' % bar_frac)
        cluster_width_def = latex_length('clusterwidth', '%f\\barwidth' % cluster_width_bars)
        padding_def = latex_length('padding', '%f\\barwidth' % cluster_padding)
        bar_width_def.comment = 'RStack width defs'
        bar_width_def.space_before = 1
        self._definitions.append(bar_width_def)
        self._definitions.append(cluster_width_def)
        self._definitions.append(padding_def)
        
        style_key = 'bar-styles-%d' % num_bars_cluster
        if style_key in template['rstack']:
            bar_styles = template['rstack'][style_key]
        else:
            bar_styles = template['rstack']['bar-styles-n'][:num_bars_cluster]

        bar_style_comment = tikz_comment('Bar styles')
        bar_style_comment.space_before = 1
        self._definitions.append(bar_style_comment)
        for i, style in enumerate(bar_styles):
            bar_style_name = self._bar_ns[i]
            bar_style = tikz_style(bar_style_name)
            bar_style.set_option(style)
            self._definitions.append(bar_style)

        # plot the bars
        bar_comment = tikz_comment('Bars')
        bar_comment.space_before = 1
        self._plot_elements.append(bar_comment)

        #base = '0' if self.ymin <= 0 else '\\ymin'
        if self.ymin != 0:
            raise RuntimeError('Invalid base for row stack?')

        for i, (key, values) in enumerate(self._clusters):
            base = 0
            offset = '%d\\clusterwidth + \\padding' % (i)
            for j, value in enumerate(values):
                p1 = '(%s, %f)' % (offset, base)
                p2 = '++(\\barwidth, %s)' % value
                white_bar = tikz_rectangle(p1, p2)
                white_bar.set_option('fill', 'white')
                real_bar = tikz_rectangle(p1, p2)
                real_bar.set_option(self._bar_ns[j])
                self._plot_elements.append(white_bar)
                self._plot_elements.append(real_bar)
                base = base + float(value)

                
    def _get_xtics(self):
        xtics = []
        for i, (key, values) in enumerate(self._clusters):
            loc = '%f\\clusterwidth' % (i + 0.5)
            xtics.append((loc, key))
        return xtics

    def _get_legends(self):
        legends = []
        for i, column in enumerate(self._column_header):
            style = self._bar_ns[i]
            legends.append((style, column))
        return legends
