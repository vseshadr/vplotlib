"""This file defines a TikZ picture class which maps to the tikzpicture
enviroment

"""


from tikz.element import TikZElement


class TikZPicture(TikZElement):

    """Implements the functionality to render a tikzpicture enviroment. A
    picture is modelled as a list of "picturable" elements. Elements are
    rendered in the order in which they are added to the picture. The client is
    reponsible for ensuring that name dependencies are met while adding
    elements.

    Parameters:
    elements -- list of elements that constitute the picture

    """

    def __init__(self):
        """Construct an empty picture"""
        TikZElement.__init__(self)
        self.nodable = True
        self.elements = []

    def add_element(self, element):
        """Add an element to the element list"""
        if not element.picturable:
            raise RuntimeError('Element is not picturable')
        self.elements.append(element)

    def __str__(self):
        """Generate and return the code to render the picture"""
        element_string = '\n'.join(element.render() for element in self.elements)
        # add indentation
        element_string = element_string.replace('\n', '\n  ')
        return """\
\\begin{tikzpicture}[%s]
  %s
\\end{tikzpicture}""" % (self.option_string(), element_string)
