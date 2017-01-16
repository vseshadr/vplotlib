"""This file defines the TikZ shape class and also many related shapes"""

from tikz.element import TikZElement


# Available line types in TikZ
tikz_line_types = [
    'solid',
    'dashed',
    'dotted',
    'densely dashed',
    'densely dotted',
]

# Available thicknesses in TikZ
tikz_thicknesses = [
    'ultra thin',
    'very thin',
    'thin',
    'semithick',
    'thick',
    'very thick',
    'ultra thick',
]

class TikZCoordinate(TikZElement):

    """Wrapper for the TikZ \coordinate"""

    def __init__(self, name=None, point=None):
        """Construct a new TikZ Coordinate"""
        TikZElement.__init__(self)
        self._name = name
        self._point = point
        self.picturable = True


    def name(self, name):
        self._name = name
        
    def point(self, point):
        self._point = point

    def __str__(self):
        if self._point is None:
            raise RuntimeError('Invalid coordinate point')
        if self._name is None:
            raise RuntimeError('Invalid coordinate name')
        
        return '\\coordinate (%s) at %s;' % (self._name, self._point)
        

class TikZShape(TikZElement):

    """Implements a abstract shape class that is inherited by all other shapes.

    Parameters:
    line_type -- the type of the line (border) e.g., solid, dashed, dotted
    thickness -- thickness of the line, outline
    style     -- predefined style for the shape

    Any shape inheriting this class should call the finalize function within its
    __str__ function.

    """

    def __init__(self, line_type=None, thickness=None, style=None):
        """Construct a shape with the given line type, thickness and style"""
        TikZElement.__init__(self)
        self.picturable = True
        self.line_type = line_type
        self.thickness = thickness
        self.style = style

    ## FIX ME: There should be better way of implementing this function rather
    ## than have all the inheriters call it explicitly
    def finalize(self):

        """Validate the line type and thickness if specified and also set the
        corresponding options

        """

        if self.style is not None:
            self.options[self.style] = ''

        if self.line_type is not None:
            if self.line_type not in tikz_line_types:
                raise RuntimeError("`%s' is not a valid TikZ line type" %
                                   self.line_type)
            self.options[self.line_type] = ''

        if self.thickness is not None:
            if self.thickness not in tikz_thicknesses:
                raise RuntimeError("`%s' is not a valid TikZ thickness" %
                                   self.thickness)
            self.options[self.thickness] = ''


class TikZLine(TikZShape):

    """Implements the functionality to render a line.

    Parameters:
    p1        -- end point 1
    p2        -- end point 2
    connector -- how should the two points be connected? direct line or manhattan?

    """

    def __init__(self, p1=None, p2=None, connector='--'):
        TikZShape.__init__(self)
        self.p1 = p1
        self.p2 = p2
        self.connector = connector

    def __str__(self):
        if self.p1 is None:
            raise RuntimeError('End point 1 not specified for the line')
        if self.p2 is None:
            raise RuntimeError('End point 2 not specified for the line')
        TikZShape.finalize(self)
        return '\\draw [%s] %s %s %s;' % (self.option_string(), self.p1,
                                        self.connector, self.p2)


class TikZRectangle(TikZLine):

    """Implements the functionality to render a rectangle.

    A rectangle is just a line with connector = rectangle. Look at the TikZLine
    class for the other parameters.

    """

    def __init__(self, p1=None, p2=None):
        """Construct a rectangle with the given end points"""
        TikZLine.__init__(self, p1, p2)
        self.connector = 'rectangle'


class TikZCircle(TikZShape):

    """Implements the functionality to render a circle.

    Parameters:
    center -- center point
    radius -- radius

    """

    def __init__(self, center=None, radius=None):
        """Construct a circle with the given center and radius"""
        TikZShape.__init__(self)
        self.center = center
        self.radius = radius

    def __str__(self):
        if self.center is None:
            raise RuntimeError('Circle needs to have a center')
        if self.radius is None:
            raise RuntimeError('Circle needs to have a radius')
        TikZShape.finalize(self)
        return '\\draw [%s] %s circle(%s);' % (self.option_string(),
                                               self.center, self.radius)


class TikZPath(TikZShape):

    """Implements the functionality to render a path.

    A path is a series of points with successive points connected by a line
    segment.

    Parameters:
    points -- list of points

    """

    def __init__(self, points=None):
        """Construct a path with given points"""
        TikZShape.__init__(self)
        self.points = [] if points is None else points

    def __str__(self):
        if not self.points:
            raise RuntimeError('No points in the path')
        TikZShape.finalize(self)
        return '\\draw [%s] %s;' % (self.option_string(),
                                    ' -- '.join(str(point)
                                                for point in self.points))
