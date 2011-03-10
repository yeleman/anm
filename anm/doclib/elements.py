#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


class PageBreak(object):
    def __init__(self):
        pass


class Text(object):

    DEFAULT_SIZE = 10

    def __init__(self, text, italic=False, bold=False,
                 size=DEFAULT_SIZE):
        self.text = text
        self.italic = italic
        self.bold = bold
        self.size = size


class Paragraph(object):
    '''
        A paragraph represents a single paragraph in a document.
        It can either be a single string, or a list of Text objects
        if you want the paragraph to have different styles within
        the same block of text.

        Examples:
            Paragraph(u'My first sentence.  My second sentence.')
            Paragraph(Text('My bold paragraph', bold=True))
            Paragraph([
                Text('Bold sentence. ', bold=True),
                Text('Italic sentence. ', italic=True)])

    '''

    def __init__(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            self.contents = [Text(text)]
        elif isinstance(text, Text):
            self.contents = [text]
        elif isinstance(text, list):
            self.contents = text
        else:
            raise ValueError('Invalid arg')


class HLine(object):

    def __init__(self):
        pass


class Section(Text):
    def __init__(self, text):
        Text.__init__(self, text)


class Document(object):

    def __init__(self,
            title,
            subtitle=None,
            landscape=False,
            stick_sections=False,
            datestring=u'Generated on %d-%m-%Y at %H:%M.'):

        self.title = title
        self.subtitle = subtitle
        self.landscape = landscape
        self.stick_sections = stick_sections
        self.datestring = datestring
        self.contents = []

    def add_element(self, element):
        self.contents.append(element)


class TableDataError(Exception):
    pass


class InvalidRowError(TableDataError):
    pass


class InvalidCellError(TableDataError):
    pass


class Table(object):

    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER = 2
    ALIGN_JUSTIFY = 3

    def __init__(self, ncols, title=None):
        ''' Optional: Text object -- title of table to be
            printed as a header over the table
        '''
        if title is not None:
            self.title = self._text_or_error(title)
        else:
            self.title = None

        ''' Number of columns in the table '''
        self.ncols = ncols

        ''' List of (bool, [col data]) tuples
            where bool indicates whether it's a
            header row and data is the column
            contents.  The contents must be
            Text objects.
        '''
        self.rows = []

        self.column_widths = {}
        self.column_alignments = {}

    def add_header_row(self, values):
        if len(values) != self.ncols:
            raise InvalidRowError
        values = map(self._text_or_error, values)
        self.rows.append((True, values))

    def add_row(self, values):
        if len(values) != self.ncols:
            raise InvalidRowError
        values = map(self._text_or_error, values)
        self.rows.append((False, values))

    def _text_or_error(self, obj):
        if not isinstance(obj, Text):
            raise InvalidCellError
        return obj

    def set_alignment(self, alignment, column):
        """ set alignment for a particular column/row """
        self.column_alignments[column] = alignment

    def set_column_width(self, width, column):
        """ set width (in % of total) of a particular column """
        self.column_widths[column] = width
