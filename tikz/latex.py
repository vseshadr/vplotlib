"""This file defines some latex specific elements."""

from tikz.element import TikZElement


# latex font size map
latex_font_map = {
    'tiny'     : '\\tiny',
    'script'   : '\\scriptsize',
    'footnote' : '\\footnotesize',
    'small'    : '\\small',
    'normal'   : '\\normalsize',
    'large'    : '\\large',
    'Large'    : '\\Large',
    'LARGE'    : '\\LARGE',
    'huge'     : '\\huge',
}


class LatexText(TikZElement):

    """Defines the interface to render text in a plot"""

    def __init__(self, text=None, font_size='normal'):
        """Create a new text with the specified font size"""
        TikZElement.__init__(self)
        self.nodable = True
        self.text = text
        self.font_size = font_size

    def __str__(self):
        """Generate and return the string to render the text"""
        font_size = latex_font_map[self.font_size] if \
            self.font_size in latex_font_map else self.font_size
        return '%s{%s}' % (font_size, self.text)


class LatexMinipage(TikZElement):

    """Defines the interface to render a minipage"""

    def __init__(self, text=None, font_size='normal', width=None):
        """Create a new minipage with the given text, font size and width"""
        TikZElement.__init__(self)
        self.nodable = True
        self.text = text
        self.font_size = font_size
        self.width = width

    def __str__(self):
        """Generate and return the string to render the minipage"""
        font_size = latex_font_map[self.font_size] if \
            self.font_size in latex_font_map else self.font_size
        return """\
\\begin{minipage}{%s}
  \\centering
  %s{%s}
\\end{minipage}""" % (self.width, font_size, self.text)


class LatexDef(TikZElement):

    """Defines the interface to create a latex definition"""

    def __init__(self, name=None, value=None):
        """Create a new definition with the given name and value."""
        TikZElement.__init__(self)
        self.nodable = True
        self.picturable = True
        self.name = name
        self.value = value

    def __str__(self):
        """Generate and return the string to render the definition"""
        return '\\def \\%s {%s}' % (self.name, self.value)


class LatexLength(TikZElement):

    """Defines the interface to create a new length field. A length field has a
    name, starting value and a set of additions. Lengths are immutable. Once
    initialized to a value, it cannot be update at a later point."""

    def __init__(self, name=None, value=None):
        """Create a new length field with the specified name and length"""
        TikZElement.__init__(self)
        self.nodable = True
        self.picturable = True
        self.name = name
        self.value = value
        self.additions = []

    def add(self, value):
        """Add the value to the list of additions"""
        self.additions.append(value)
        
    def __str__(self):
        """Generate and return the string to render the length definition"""
        add_string = ''.join('\n\\addtolength{\\%s}{%s}' % (self.name, addition)
                             for addition in self.additions)
        return """\
\\newlength{\\%s}
\\setlength{\\%s}{%s}%s""" % (self.name, self.name, self.value, add_string)
