"""This file implements a simple comment"""


from tikz.element import TikZElement


class TikZComment(TikZElement):

    """Implements a simple comment to be added to the TikZ code"""

    def __init__(self, comment=None):
        """Create a new comment. Comments do not have options"""
        TikZElement.__init__(self)
        self.picturable = True
        self.comment = comment

    def __str__(self):
        """Comments have no 'other' strings"""
        return ''
