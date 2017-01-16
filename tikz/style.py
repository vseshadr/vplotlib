"""This file implements a TikZ style class"""

from tikz.element import TikZElement


class TikZStyle(TikZElement):

    """Implements the functionality to render a style. A style has a name and a
    set of options.

    Parameters:
    name -- name of the style

    """

    def __init__(self, name=None):
        """Constructs a new style with the given name"""
        TikZElement.__init__(self)
        self.picturable = True
        self.name = name

    def __str__(self):
        """Generate and return the string to render the style"""
        return '\\tikzset{%s/.style={%s}};' % (self.name, self.option_string())
