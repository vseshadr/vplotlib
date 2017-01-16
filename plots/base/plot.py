"""A generic plot class."""

from tikz.picture import TikZPicture as tikz_picture
from tikz.node import TikZNode as tikz_node
from tikz.style import TikZStyle as tikz_style

from tikz.shapes import TikZRectangle as tikz_rectangle
from tikz.shapes import TikZLine as tikz_line
from tikz.shapes import TikZCoordinate as tikz_coord

from tikz.latex import LatexLength as latex_length
from tikz.latex import LatexDef as latex_def
from tikz.latex import LatexText as latex_text
from tikz.latex import LatexMinipage as latex_minipage
from tikz.latex import latex_font_map as lfm

from helper.helper import ffloat
from helper.helper import gen_tics

from plots.base.legend import Legend

class Plot:

    """Defines an abstract plot."""

    def __init__(self):

        self.title = None
        self.xlabel = None
        self.ylabel = None

        self.ymax = None
        self.ymin = None
        self.ystep = None
        self.ypercent = False
        self.opt_tics=10

        self.xmax = None
        self.xmin = None
        self.xstep = None

        self._has_ytics = False
        self._ycontinuous = False
        self._yscale = 1
        self._ytics_all = False
        self._auto_ytics = False

        self._has_xtics = False
        self._xcontinuous = False
        self._xscale = 1
        self._xtics_all = False
        self._auto_xtics = False

        self._has_legend = False
        self._legend_type = None

        self._definitions = []
        self._plot_elements = []


    def plot(self, template):

        plot_area_height = template['plot-area']['height']
        plot_area_width = template['plot-area']['width']

        # set up major axis
        if self._ycontinuous:
            self.ymax = self._get_ymax() if self.ymax is None else self.ymax
            self.ymin = self._get_ymin() if self.ymin is None else self.ymin
            self._yscale = float(plot_area_height) / (self.ymax - self.ymin)

        if self._has_ytics:
            ytics = None
            if self._auto_ytics:
                if not self._ycontinuous:
                    raise RuntimeError('Auto requires continuity')
                if self.ymax <= self.ymin:
                    raise RuntimeError('Invalid y-range')
                ytics = gen_tics(self.ymin, self.ymax, self.ystep, self.opt_tics)
            if ytics is None:
                ytics = self._get_ytics()
            if not self._ytics_all: ytics = ytics[1:-1]
            
        # set up minor axis
        if self._xcontinuous:
            self.xmax = self._get_xmax() if self.xmax is None else self.xmax
            self.xmin = self._get_xmin() if self.xmin is None else self.xmin
            self._xscale = float(plot_area_width) / (self.xmax - self.xmin)

        if self._has_xtics:
            xtics = None
            if self._auto_xtics:
                if not self._xcontinuous:
                    raise RuntimeError('Auto requires continuity')
                if self.xmax <= self.xmin:
                    raise RuntimeError('Invalid y-range')
                xtics = gen_tics(self.xmin, self.xmax, self.xstep)
            if xtics is None:
                xtics = self._get_xtics()
            if not self._xtics_all: xtics = xtics[1:-1]

        if not template['xtics']['display']: self._has_xtics = False
            
        # general styles
        nopadding = tikz_style('no padding')
        nopadding.set_option('inner sep', '0')
        nopadding.set_option('outer sep', '0')
        nopadding.space_before = 1
        nopadding.space_after = 1
        nopadding.comment = 'Style for no padding'
        self._definitions.append(nopadding)

        # add general defs
        plot_height_def = latex_length('plotheight', '%scm' %
                                       template['plot-area']['height'])
        plot_width_def = latex_length('plotwidth',  '%scm' %
                                      template['plot-area']['width'])

        if self._ycontinuous:
            ymin = ffloat(self.ymin)
            ymax = ffloat(self.ymax)
        else:
            ymin = '0'
            ymax = '\\plotheight'

        if self._xcontinuous:
            xmin = ffloat(self.xmin)
            xmax = ffloat(self.xmax)
        else:
            xmin = '0'
            xmax = '\\plotwidth'

        ymin_def = latex_def('ymin', ymin)
        ymax_def = latex_def('ymax', ymax)
        xmax_def = latex_def('xmax', xmax)
        xmin_def = latex_def('xmin', xmin)
        
        self._definitions.append(plot_height_def)
        self._definitions.append(plot_width_def)
        self._definitions.append(ymin_def)
        self._definitions.append(ymax_def)
        self._definitions.append(xmin_def)
        self._definitions.append(xmax_def)

        # title related defs
        if self.title is not None:
            title_def = latex_def('plottitle', self.title)
            title_font_def = latex_def('titlefontsize',
                                       lfm[template['title']['font-size']])
            title_def.comment = 'Plot title defs'
            title_def.space_before = 1
            self._definitions.append(title_def)
            self._definitions.append(title_font_def)

        # ylabel related defs
        if self.ylabel is not None:
            ylabel_def = latex_def('plotylabel', self.ylabel)
            ylabel_font_def = latex_def('ylabelfontsize',
                                       lfm[template['ylabel']['font-size']])
            ylabel_def.comment = 'Plot Y-label defs'
            ylabel_def.space_before = 1
            self._definitions.append(ylabel_def)
            self._definitions.append(ylabel_font_def)

        # xlabel related defs
        if self.xlabel is not None:
            xlabel_def = latex_def('plotxlabel', self.xlabel)
            xlabel_font_def = latex_def('xlabelfontsize',
                                       lfm[template['xlabel']['font-size']])
            xlabel_def.comment = 'Plot X-label defs'
            xlabel_def.space_before = 1
            self._definitions.append(xlabel_def)
            self._definitions.append(xlabel_font_def)

        # ytics related defs
        if self._has_ytics and template['ytics']['display']:
            ytics_font_def = latex_def('yticsfontsize',
                                       lfm[template['ytics']['font-size']])
            ytics_font_def.comment = 'Plot ytics defs'
            ytics_font_def.space_before = 1
            ytics_width_def = latex_def('yticswidth', '%smm' % template['ytics']['width'])

            ytic_style = tikz_style('ytic')
            ytic_style.set_option('xshift', '-%smm' % template['ytics']['label-shift'])
            ytic_style.set_option('anchor', 'east')
            ytic_style.set_option('inner xsep', '0.75mm')

            self._definitions.append(ytics_font_def)
            self._definitions.append(ytics_width_def)
            self._definitions.append(ytic_style)

            if template['ytics']['help-lines']:
                help_line_style = tikz_style('y-help-line')
                help_line_style.set_option('thin')
                help_line_style.set_option('densely dotted')
                self._definitions.append(help_line_style)

        # xtics related defs
        if self._has_xtics and template['xtics']['display']:
            xtics_font_def = latex_def('xticsfontsize',
                                       lfm[template['xtics']['font-size']])
            xtics_font_def.comment = 'Plot xtics defs'
            xtics_font_def.space_before = 1
            xtics_width_def = latex_def('xticswidth', '%smm' % template['xtics']['width'])

            xtic_style = tikz_style('xtic')
            xtic_style.set_option('inner ysep', '0.75mm')
            if template['xtics']['rotate'] is None or template['xtics']['rotate'] == 0:
                xtic_style.set_option('anchor', 'base')
                xtic_style.set_option('yshift', '-%smm' % (template['xtics']['label-shift'] + 1))
            else:
                xtic_style.set_option('anchor', 'east')
                xtic_style.set_option('xshift', '-%smm' % template['xtics']['label-shift'])
                xtic_style.set_option('rotate', template['xtics']['rotate'])
            
            self._definitions.append(xtics_font_def)
            self._definitions.append(xtics_width_def)
            self._definitions.append(xtic_style)

            if template['xtics']['help-lines']:
                help_line_style = tikz_style('x-help-line')
                help_line_style.set_option('thin')
                help_line_style.set_option('densely dotted')
                self._definitions.append(help_line_style)
                
            
        # plot area picture
        plot_area_picture = tikz_picture()
        plot_area_picture.set_option('yscale', self._yscale)
        plot_area_picture.set_option('xscale', self._xscale)

        # anchors
        swanchor = '(\\xmin, \\ymin)'
        neanchor = '(\\xmax, \\ymax)'
        south_west_anchor = tikz_line(swanchor, swanchor)
        north_east_anchor = tikz_line(neanchor, neanchor)
        plot_area_picture.add_element(south_west_anchor)
        plot_area_picture.add_element(north_east_anchor)

        # help lines
        if self._has_ytics and template['ytics']['help-lines']:
            for loc, label in ytics:
                help_line = tikz_line('(\\xmin, %s)' % loc, '(\\xmax, %s)' % loc)
                help_line.set_option('y-help-line')
                plot_area_picture.add_element(help_line)
        if self._has_xtics and template['xtics']['help-lines'] and template['xtics']['display']:
            for loc, label in xtics:
                help_line = tikz_line('(%s, \\ymin)' % loc, '(%s, \\ymax)' % loc)
                help_line.set_option('x-help-line')
                plot_area_picture.add_element(help_line)

        # append plot elements
        self._get_plot_area(template)
        for element in self._plot_elements: plot_area_picture.add_element(element)
        
        plot_area_node = tikz_node(name='plotarea', content=plot_area_picture)
        plot_area_node.location = '(0, 0)'
        plot_area_node.set_option('anchor', 'south west')
        plot_area_node.set_option('no padding')
        plot_area_node.comment = 'Plot area node'
        plot_area_node.space_before = 1

        # legend defs
        if self._has_legend and template['legend']['display']:
            legends = self._get_legends()

            ltemplate = template['legend']
            legend = Legend(self._legend_type, legends, ltemplate)
            legend_defs, legend_picture = legend.legend_picture()

            self._definitions += legend_defs

            legend_node = tikz_node(name='legend', content=legend_picture)

            leg_location = ltemplate['location']
            leg_relative = ltemplate['relative']
            leg_xshift = '%smm' % ltemplate['xshift']
            leg_yshift = '%smm' % ltemplate['yshift']
            hpadding = '%smm' % ltemplate['hpadding']
            vpadding = '%smm' % ltemplate['vpadding']

            legend_node.location = plot_area_node.position(leg_location)
            if leg_relative == 'inside':
                legend_node.set_option('anchor', leg_location)
                
                if leg_location == 'north west':
                    leg_yshift = '-' + leg_yshift
                elif leg_location == 'north east':
                    leg_yshift = '-' + leg_yshift
                    leg_xshift = '-' + leg_xshift
                elif leg_location == 'south east':
                    leg_xshift = '-' + leg_xshift
                elif leg_location == 'south west':
                    pass
                else:
                    raise RuntimeError('Invalid legend positioning')

            elif leg_relative == 'outside-h':
                leg_yshift = '0'
                if leg_location == 'north west': 
                    legend_node.set_option('anchor', 'north east')
                    leg_xshift = '-' + leg_xshift
                elif leg_location == 'north east':
                    legend_node.set_option('anchor', 'north west')
                elif leg_location == 'south east':
                    legend_node.set_option('anchor', 'south west')
                elif leg_location == 'south west':
                    legend_node.set_option('anchor', 'south east')
                    leg_xshift = '-' + leg_xshift
                else:
                    raise RuntimeError('Invalid legend positioning')

            elif leg_relative == 'outside-v':
                leg_xshift = '0'
                if leg_location == 'north west': 
                    legend_node.set_option('anchor', 'south west')
                elif leg_location == 'north east':
                    legend_node.set_option('anchor', 'south east')
                elif leg_location == 'south east':
                    legend_node.set_option('anchor', 'north east')
                    leg_yshift = '-' + leg_yshift
                elif leg_location == 'south west':
                    legend_node.set_option('anchor', 'north west')
                    leg_yshift = '-' + leg_yshift
                else:
                    raise RuntimeError('Invalid legend positioning')

            else:
                raise RuntimeError('Invalid relative position of legend')

            legend_node.set_option('xshift', leg_xshift)
            legend_node.set_option('yshift', leg_yshift)
            legend_node.set_option('outer sep', '0')
            legend_node.set_option('inner xsep', hpadding)
            legend_node.set_option('inner ysep', vpadding)
            legend_node.set_option('fill=white')
            legend_node.set_option('draw')

        
        # ytics node
        if self._has_ytics:
            ytics_picture = tikz_picture()
            ytics_picture.set_option('yscale', self._yscale)
            
            ytics_bottom = '(0, \\ymin)'
            ytics_top = '(0, \\ymax)'
            ytics_bottom_anchor = tikz_line(ytics_bottom, ytics_bottom)
            ytics_top_anchor = tikz_line(ytics_top, ytics_top)
            ytics_picture.add_element(ytics_bottom_anchor)
            ytics_picture.add_element(ytics_top_anchor)

            tic_shift = '++(-\\yticswidth,0)'
            for loc, label in ytics:
                tic_loc = '(0, %s)' % loc
                tic = tikz_line(tic_loc, tic_shift)
                ytics_picture.add_element(tic)
                label = label + '\\%' if self.ypercent else label
                label_text = latex_text(label, '\\yticsfontsize')
                tic_label = tikz_node(content=label_text, oneline=True)
                tic_label.location = '(-\\yticswidth, %s)' % loc
                tic_label.set_option('ytic')
                ytics_picture.add_element(tic_label)

            
            ytics_node = tikz_node(name='ytics', content=ytics_picture)
            ytics_node.location = '(0, 0)'
            ytics_node.set_option('anchor', 'south east')
            ytics_node.set_option('no padding')

        # xtics node
        if self._has_xtics and template['xtics']['display']:
            xtics_picture = tikz_picture()
            xtics_picture.set_option('xscale', self._xscale)
            
            xtics_left = '(\\xmin, 0)'
            xtics_right = '(\\xmax, 0)'
            xtics_left_anchor = tikz_line(xtics_left, xtics_left)
            xtics_right_anchor = tikz_line(xtics_right, xtics_right)
            xtics_picture.add_element(xtics_left_anchor)
            xtics_picture.add_element(xtics_right_anchor)

            tic_shift = '++(0,-\\xticswidth)'
            for loc, label in xtics:
                tic_loc = '(%s, 0)' % loc
                tic = tikz_line(tic_loc, tic_shift)
                xtics_picture.add_element(tic)
                label_text = latex_text(label, '\\xticsfontsize')
                tic_label = tikz_node(content=label_text, oneline=True)
                tic_label.location = '(%s, -\\xticswidth)' % loc
                tic_label.set_option('xtic')
                xtics_picture.add_element(tic_label)

            
            xtics_node = tikz_node(name='xtics', content=xtics_picture)
            xtics_node.location = '(0, 0)'
            xtics_node.set_option('anchor', 'north west')
            xtics_node.set_option('no padding')

        # ylabel node
        if self.ylabel is not None:
            ylabel_text = latex_minipage('\\plotylabel', '\\ylabelfontsize',
                                         '\\plotheight')
            ylabel_node = tikz_node(name='ylabel', content=ylabel_text)
            if self._has_ytics:
                ylabel_node.location = ytics_node.west()
                ylabel_node.set_option('no padding')
            else:
                ylabel_node.location = plot_area_node.west()
                ylabel_node.set_option('inner ysep', '0.75mm')
            ylabel_node.set_option('rotate', '90')
            ylabel_node.set_option('anchor', 'south')
            if template['ylabel']['xshift'] is not None:
                ylabel_node.set_option('yshift', '%gmm' % template['ylabel']['xshift'])

        # xlabel node
        if self.xlabel is not None:
            xlabel_text = latex_minipage('\\plotxlabel', '\\xlabelfontsize',
                                         '\\plotwidth')
            xlabel_node = tikz_node(name='xlabel', content=xlabel_text)
            if self._has_xtics and template['xtics']['display']:
                xlabel_node.location = xtics_node.south()
                xlabel_node.set_option('no padding')
            else:
                xlabel_node.location = plot_area_node.south()
                xlabel_node.set_option('inner ysep', '0.75mm')
            xlabel_node.set_option('anchor', 'north')
            if template['xlabel']['yshift'] is not None:
                xlabel_node.set_option('yshift', '-%gmm' % template['xlabel']['yshift'])

        # title node
        if self.title is not None:
            title_text = latex_minipage('\\plottitle', '\\titlefontsize',
                                         '\\plotwidth')
            title_node = tikz_node(name='title', content=title_text)
            title_node.location = plot_area_node.north()
            title_node.set_option('anchor', 'south')
            title_node.set_option('inner ysep', '0.75mm')
            if template['title']['yshift'] is not None:
                title_node.set_option('yshift', '%gmm' % template['title']['yshift'])
            
            
        outer_box = tikz_rectangle('(0, 0)', '(\\plotwidth, \\plotheight)')
        outer_box.comment = 'Outer box'
        outer_box.space_before = 1

        # Finalize
        plot = tikz_picture()
        for definition in self._definitions: plot.add_element(definition)
        plot.add_element(outer_box)
        plot.add_element(plot_area_node)
        if self._has_legend and template['legend']['display']: plot.add_element(legend_node)
        if self._has_ytics: plot.add_element(ytics_node)
        if self._has_xtics: plot.add_element(xtics_node)
        if self.ylabel is not None: plot.add_element(ylabel_node)
        if self.xlabel is not None: plot.add_element(xlabel_node)
        if self.title is not None: plot.add_element(title_node)
        return plot

    def load_data(self, string):
        raise RuntimeError('What will one plot without any data')

    def _get_ymax(self):
        raise RuntimeError('Unimplemented function. Need routine to compute ymax')

    def _get_ymin(self):
        raise RuntimeError('Unimplemented function. Need routine to compute ymin')

    def _get_xmax(self):
        raise RuntimeError('Unimplemented function. Need routine to compute xmax')

    def _get_xmin(self):
        raise RuntimeError('Unimplemented function. Need routine to compute xmin')


    def _get_ytics(self):
        raise RuntimeError('Unimplemented function. Need routine to get ytics')

    def _get_xtics(self):
        raise RuntimeError('Unimplemented function. Need routine to get xtics')

    def _get_plot_area(self, template):
        """Function to return the plot area."""
        pass

    def _get_legends(self):
        """Function to get the legends."""
        raise RuntimeError('If legend, return legend')
