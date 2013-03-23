#!/usr/bin/env python
# --dbohdan 2013.03.23
'''
This module converts CSV files into HTML tables. It can be used as a standalone
program or imported from your Python code.

For best results install https://pypi.python.org/pypi/html.
See the files README.md and LICENSE for more information.
'''
from __future__ import print_function

import csv
import argparse


DEFAULT_DELIMITER = ";"

# Exit status constants
NO_FILE_GIVEN = 1
IO_ERROR = 2
CANNOT_IMPORT_MODULES = 3
UNKNOWN_ERROR = 127


# Below are classes for interfacing with different HTML output modules.
class TableGen(object):
    '''Parent class for module-interfacing classes.'''

    def __init__(self, title="", completedoc=False):
        self.completedoc = completedoc
        self.html = None
        self.table = None

    def __str__(self):
        if self.completedoc:
            return str(self.html)
        else:
            return str(self.table)


class TableGenHTMLgen(TableGen):
    '''Interface for the module HTMLgen for generating tables.'''

    def __init__(self, title="", completedoc=False):
        super(TableGenHTMLgen, self).__init__(title, completedoc)
        self.table = HTMLgen.Table(title)
        self.table.body = []
        if self.completedoc:
            self.html = HTMLgen.SimpleDocument(title=title)
            self.html.append(self.table)

    def heading(self, hrow):
        '''Specifies the table''s heading. This should be only called one
        before any rows are added.'''
        self.table.heading = hrow

    def add(self, row):
        'Adds a row to the table; trow should be an iterable.'
        self.table.body.append([x if x != '' else '&nbsp;' for x in row])


class TableGenHtml(TableGen):
    '''Interface for the module html for generating tables.'''

    def __init__(self, title='', completedoc=False):
        super(TableGenHtml, self).__init__(title, completedoc)
        if self.completedoc:
            self.html = html.HTML('html')
            # self.html.text('<!DOCTYPE html>', escape=False)
            self.html.head.title(title)
            self.table = self.html.body.table(border='1')
        else:
            self.html = html.HTML()
            self.table = self.html.table(border='1')

    def heading(self, headerrow):
        '''Specifies the table''s heading. This should be only called one
        before any rows are added.'''
        newtr = self.table.tr
        for item in headerrow:
            if item != '':
                newtr.th(item)
            else:
                newth = newtr.th
                newth.text('&nbsp;', escape=False)

    def __str__(self):
        if self.completedoc:
            return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" \
"http://www.w3.org/TR/html4/strict.dtd">\n' + str(self.html)
        else:
            return str(self.table)

    def add(self, tablerow):
        'Adds a row to the table; trow should be an iterable.'
        newtr = self.table.tr
        for item in tablerow:
            if item != '':
                newtr.td(item)
            else:
                newtd = newtr.td
                newtd.text('&nbsp;', escape=False)


def convert_csv_to_html(inputstream, outputstream, title='',
                        delim=DEFAULT_DELIMITER, nstart=0, skipheader=False,
                        renum=False, completedoc=False, usehtmlgen=False):
    '''
    Takes CSV from inputstream (an iterable) and outputs an HTML table to
    outputstream (anything with a write method that takes a string).
    '''

    # The imports below are necessary when calling this function from an
    # external module. They do not hurt performance when csv2html is used as
    # a standalone program.
    if usehtmlgen:
        global HTMLgen
        import HTMLgen
        tablegen = TableGenHTMLgen(title, completedoc)
    else:
        global html
        import html
        tablegen = TableGenHtml(title, completedoc)

    # Read the CSV stream and output HTML.
    csvreader = csv.reader(inputstream, dialect='excel',
                           delimiter=delim)
    nrow = 0  # row number counter
    headerrow = not skipheader

    for row in csvreader:
        if headerrow:
            tablegen.heading(row)
            headerrow = False
        else:
            if nrow >= nstart:
                if renum:
                    row[0] = str(nrow - nstart +
                                 int(skipheader or
                                 nstart > 0))
                                 # Adds 1 if true to correct for
                                 # numbering rows from zero with no
                                 # zeroth header row or subtracting
                                 # nstart.
                tablegen.add(row)
        nrow += 1

    outputstream.write(str(tablegen))


def main():
    '''
    This function is called when the module is run as the main program.
    It handles command line options and opening files for convert_csv_to_html.
    '''

    # Configure the command line argument parser.
    parser = argparse.ArgumentParser(description='Converts CSV files into \
HTML tables')
    parser.add_argument('inputfile', help='input file',
                        default='', metavar='input')
    parser.add_argument('-o', '--output', help='output file',
                        default='', required=False, metavar='output',
                        dest='outputfile')
    parser.add_argument('-t', '--title', help='document & table title',
                        default='')
    parser.add_argument('-d', '--delimiter', help='field delimiter for CSV \
("%s" by default)' % DEFAULT_DELIMITER, default=DEFAULT_DELIMITER,
                        dest='delim')
    parser.add_argument('-s', '--start', metavar='N', help=
                        'skip the first N-1 rows, start with row N',
                        type=int, default=0, dest='nstart')
    parser.add_argument('-r', '--renumber', help=
                        'replace the first column with row numbers',
                        action='store_true', default=False, dest='renum')
    parser.add_argument('-n', '--no-header', help=
                        'do not use the first row of the input as the header',
                        action='store_true', default=False, dest='skipheader')
    parser.add_argument('-c', '--complete-document', help=
                        'output a complete HTML document instead of only the \
    table', action='store_true', default=False, dest='completedoc')
    parser.add_argument('-g', '--force-htmlgen', help=
                        'uses HTMLgen even if the html module is available',
                        action='store_true', default=False,
                        dest='forcehtmlgen')

    # Process command line arguments.
    args = parser.parse_args()

    if args.inputfile == '':
        parser.print_help()
        exit(NO_FILE_GIVEN)

    if args.outputfile == '':
        args.outputfile = '/dev/stdout'

    # Import HTML output modules.
    usinghtmlgen = args.forcehtmlgen

    if not usinghtmlgen:
        global html
        try:
            import html
        except ImportError:
            usinghtmlgen = True

    if usinghtmlgen:  # Careful, do _not_ merge this with the above block.
        global HTMLgen
        try:
            import HTMLgen
        except ImportError:
            if args.forcehtmlgen:
                print("Forced to use HTMLgen but couldn't import it.\n\n\
Please install HTMLgen.")
            else:
                print("Couldn't import HTMLgen or html.\n\n\
Please install either to use csv2html.")
            exit(CANNOT_IMPORT_MODULES)

    try:
        with open(args.inputfile, 'rb') as incsvfile:
            with open(args.outputfile, 'wb') as outhtmlfile:
                convert_csv_to_html(incsvfile, outhtmlfile, args.title,
                                    args.delim, args.nstart, args.skipheader,
                                    args.renum, args.completedoc,
                                    usinghtmlgen)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(IO_ERROR)
    except Exception as e:
        print("Unexpected error:", e)
        exit(UNKNOWN_ERROR)


if __name__ == '__main__':
    main()

