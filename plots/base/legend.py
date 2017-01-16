"""Generate legends for plots"""

from math import ceil

from tikz.picture import TikZPicture as tikz_picture
from tikz.node import TikZNode as tikz_node
from tikz.style import TikZStyle as tikz_style

from tikz.shapes import TikZRectangle as tikz_rectangle
from tikz.shapes import TikZLine as tikz_line

from tikz.latex import LatexText as latex_text
from tikz.latex import LatexDef as latex_def
from tikz.latex import latex_font_map as lfm

class Legend:

    def __init__(self, ltype=None, legend=None, template=None):

        self._type = ltype
        self._legends = legend
        self._template = template

        

    def legend_picture(self):

        legend_ids = ['legone', 'legtwo', 'legthree', 'legfour', 'legfive',
                      'legsix', 'legseven', 'legeight', 'legnine', 'legten', 'legelv', 'legtwl']
                     
        legend_defs = []
        
        legends = self._legendify()
        num_legends = len(legends)
        rows = 0
        columns = 0

        template = self._template

        if template['arrange'] == 'horizontal':
            rows = int(template['rows'])
            columns = int(ceil(float(num_legends) / rows))
        elif template['arrange'] == 'vertical':
            columns = int(template['columns'])
            rows = int(ceil(float(num_legends) / columns))
        else:
            raise RuntimeError('Unknown legend arrangement')


        longest_legends = []
        for j in range(columns):
            longest = 0
            for i in range(rows):
                index = i*columns + j
                if index >= num_legends:
                    continue
                length = len(legends[index][1])
                longest = max(longest, length)
            longest_legends.append(longest)

        legend_fontsize_def = latex_def('legendfontsize',
                                        lfm[template['font-size']])
        legend_fontsize_def.space_before = 1
        legend_fontsize_def.comment = 'Legend defs'
        legend_defs.append(legend_fontsize_def)

        label_style = tikz_style('legend label')
        label_style.set_option('no padding')
        label_style.set_option('anchor', 'base west')
        legend_defs.append(label_style)

        legend_node_style = tikz_style('legend node')
        legend_node_style.set_option('outer sep', '0')
        legend_node_style.set_option('inner xsep', '%smm' % template['hpadding'])
        legend_node_style.set_option('inner ysep', '%smm' % template['vpadding'])
        legend_defs.append(legend_node_style)
        
        legend_nodes = []
        for i, (symbol, name) in enumerate(legends):

            name_id = legend_ids[i]
            name_var = '\\' + name_id
            name_def = latex_def(name_id, name)
            legend_defs.append(name_def)

            label_name = name_var + '\\vphantom{yg}'
            label_text = latex_text(label_name, '\\legendfontsize')
 
            column = i % columns
            longest_legend = longest_legends[column]
            phantom_name = '\\phantom{%s}' % ('{--}' * longest_legend)
            phantom_text = latex_text(phantom_name, '\\legendfontsize')

            label_node = tikz_node(content=label_text, oneline=True, location='(0,0)')
            label_node.set_option('legend label')
            phantom_node = tikz_node(content=phantom_text, oneline=True, location='(0,0)')
            phantom_node.set_option('legend label')
           
            label_picture = tikz_picture()
            label_picture.add_element(label_node)
            if columns > 1 and rows > 1:
                label_picture.add_element(phantom_node)
            label_picture.add_element(symbol)

            legend_node = tikz_node(name='%s-node' % name_id,
                                    content = label_picture)
            legend_node.set_option('legend node')

            legend_nodes.append(legend_node)

        legend_picture = tikz_picture()

        # render first row
        next_location = '(0,0)'
        for j in range(columns):
            node = legend_nodes[j]
            node.location = next_location
            next_location = node.east()
            node.set_option('anchor', 'west')
            legend_picture.add_element(node)

        # render the other rows
        for i in range(1, rows):
            for j in range(columns):
                index = i*columns + j
                if index >= num_legends: continue
                node = legend_nodes[index]
                anchor_node = legend_nodes[index - columns]
                node.location = anchor_node.south_west()
                node.set_option('anchor', 'north west')
                legend_picture.add_element(node)

        return (legend_defs, legend_picture)

    
    def _legendify(self):
        """Convert legend styles to symbols"""

        template = self._template
        size = '%smm' % template['size']
        sxshift = '-%smm' % template['symbol-xshift']
        syshift = '%smm' % template['symbol-yshift']
        
        if self._type == 'box':
            legends = []
            for (style, name) in self._legends:
                p1 = '(%s, %s)' % (sxshift, syshift)
                p2 = '++(-%s, %s)' % (size, size)
                symbol = tikz_rectangle(p1, p2)
                symbol.set_option(style)
                legends.append((symbol, name))
            return legends

        elif self._type == 'line':
            legends = []
            for (style, name) in self._legends:
                p1 = '(%s, %s)' % (sxshift, syshift)
                p2 = '++(-%s, 0)' % (size)
                symbol = tikz_rectangle(p1, p2)
                symbol.set_option(style)
                legends.append((symbol, name))
            return legends

        elif self._type == 'custom':
            return self._legends

        else:
            raise RuntimeError('Unknown legend type')
