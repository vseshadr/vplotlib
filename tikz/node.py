"""This module implements a TikZ node. This corresponds to a node in the TikZ
picture environment. A node can be used to display some text or include another
picture.

"""

from tikz.element import TikZElement


# TikZ node positions
tikz_node_positions = [
    'center',
    'north west',
    'north',
    'north east',
    'east',
    'south east',
    'south',
    'south west',
    'west',
]


class TikZNode(TikZElement):

    """Implements a TiKZ node object.

    Parameters:
    name     -- name corresponding to the node
    location -- where should the node be located in the picture
    content  -- what should be inside the node
    oneline  -- should the code be rendered in a single line (readability)

    Functions:
    position -- returns the anchor point corresponding to reference
    XXX()    -- returns position('XXX'), where XXX is one of the 9 node positions

    """

    def __init__(self, name=None, location=None, content=None, oneline=False):
        """Construct a new node with the given name, location and content"""
        TikZElement.__init__(self)
        self.picturable = True
        self.name = name
        self.location = location
        self.content = content
        self.oneline = oneline

    def position(self, reference):
        """Returns the position corresponding to the reference w.r.t to the node"""
        if reference not in tikz_node_positions:
            raise RuntimeError("`%s' is not a valid node position" %
                               (reference))
        if self.name is None:
            raise RuntimeError('Position called on node with no name')
        return '(%s.%s)' % (self.name, reference)


    def center(self):
        return self.position('center')

    def north_west(self):
        return self.position('north west')

    def north(self):
        return self.position('north')

    def north_east(self):
        return self.position('north east')

    def east(self):
        return self.position('east')

    def south_east(self):
        return self.position('south east')

    def south(self):
        return self.position('south')

    def south_west(self):
        return self.position('south west')

    def west(self):
        return self.position('west')


    def __str__(self):
        """Return the TikZ string to render the node"""
        name = '' if self.name is None else ' (%s)' % self.name
        location = '' if self.location is None else ' at %s' % self.location
        if self.content is None:
            raise RuntimeError('Node with no content?')
        if not self.content.nodable:
            raise RuntimeError('Node content should be nodable!')
        # add indentation to content
        content = str(self.content).replace('\n','\n  ')
        format_args = (name, location, self.option_string(), content)
        if self.oneline:
            return '\\node%s%s [%s] {%s};' % (format_args)
        else:
            return """\
\\node%s%s
  [%s] {
  %s
};\
""" % (format_args)
