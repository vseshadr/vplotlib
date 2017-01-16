"""This file defines the abstract TikZ element class"""


class TikZElement:

    """Defines an abstract TikZ element.

    Parameters:
    nodable      -- can the element be included inside a node?
    picturable   -- can the element be included inside a picture?
    options      -- dictionary of options for the element
    comment      -- optional comment to be prepended to the rendered string
    space_before -- number of blank lines before
    space_after  -- number of blank lines after

    The TikZ string generated for an element is of the following format:

    <space_before> number of blank lines
    % <comment>
    <str(self)>
    <space_after> number of blank lines

    """
    
    def __init__(self, options=None):
        """Constructor to create an element with a given set of options"""
        self.nodable = False
        self.picturable = False
        self.options = {} if options is None else options
        self.comment = None
        self.space_before = 0
        self.space_after = 0

    def set_option(self, key, value=''):
        """Set option the specified key and value.

        A value '' indicates no value. If value is set to None, then the key is
        ignored when the option string for the element is generated.

        """
        self.options[key] = value

    def option_string(self):
        """Generate and return the option string for the element"""
        option_list = []
        for key in sorted(self.options):
            value = self.options[key]
            if value is not None:
                option_list.append(key if value is '' else '%s=%s' % (key, value))
        return ','.join(option_list)

    def render(self):
        """Generate and return the final string to be output"""
        space_before = '\n' * self.space_before
        space_after = '\n' * self.space_after
        comment = '' if self.comment is None else '%% %s' % (self.comment)
        string = str(self)
        if len(string) and len(comment):
            string = '\n' + string
        return space_before + comment + string + space_after

    def __str__(self):
        """Generate and return the TikZ code to render the element.
        To be implemented by the inheriting classes

        """
        raise RuntimeError('String cast to be implemented by inheriting class')
    
