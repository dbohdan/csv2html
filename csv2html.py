#!/usr/bin/env python
# This software converts CSV tables into HTML tables.
# For best results install https://pypi.python.org/pypi/html.
# See the files README.md and LICENSE for more information.
# --dbohdan 2013.03.23


import csv
import os
import sys
import argparse


DEFAULT_DELIMITER = ";"

# Exit status constants
NO_FILE_GIVEN = 1
IO_ERROR = 2
CANNOT_IMPORT_MODULES = 3
UNKNOWN_ERROR = 127


# Below are classes for interfacing with different HTML output modules.
class TableGen(object):
    """Parent class for module-interfacing classes."""

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
    """Interface for the module HTMLgen for generating tables."""

    def __init__(self, title="", completedoc=False):
        super(TableGenHTMLgen, self).__init__(title, completedoc)
        self.table = HTMLgen.Table(title)
        self.table.body = []
        if self.completedoc:
            self.html = HTMLgen.SimpleDocument(title=title)
            self.html.append(self.table)

    def heading(self, h):
        self.table.heading = row

    def add(self, row):
        self.table.body.append([x if x != '' else '&nbsp;' for x in row])


class TableGenHtml(TableGen):
    """Interface for the module html for generating tables."""

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

    def heading(self, h):
        r = self.table.tr
        for item in row:
            if item != '':
                r.th(item)
            else:
                t = r.th
                t.text('&nbsp;', escape=False)

    def __str__(self):
        if self.completedoc:
            return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" \
"http://www.w3.org/TR/html4/strict.dtd">\n' + str(self.html)
        else:
            return str(self.table)

    def add(self, row):
        r = self.table.tr
        for item in row:
            if item != '':
                r.td(item)
            else:
                t = r.td
                t.text('&nbsp;', escape=False)


# Configure the command line argument parser.
parser = argparse.ArgumentParser(description=
                                 'Converts CSV files into HTML tables')
parser.add_argument('inputfile', help='input file',
                    default='', metavar='input')
parser.add_argument('-o', '--output', help='output file',
                    default='', required=False, metavar='output',
                    dest='outputfile')
parser.add_argument('-t', '--title', help='document & table title',
                    default='')
parser.add_argument('-d', '--delimiter', help='field delimiter for CSV ("%s" \
by default)' % DEFAULT_DELIMITER, default=DEFAULT_DELIMITER, dest='delim')
parser.add_argument('-s', '--start', metavar='N', help=
                    'skip the first N-1 rows, start with row N',
                    type=int, default=0, dest='nstart')
parser.add_argument('-r', '--renumber', help=
                    'replace the first column with row numbers',
                    action='store_true', default=False, dest='renum')
parser.add_argument('-k', '--skip-header', help=
                    'do not use the first row of the input as the header',
                    action='store_true', default=False, dest='skipheader')
parser.add_argument('-c', '--complete-document', help=
                    'output the code for a complete HTML document instead of \
only for the table', action='store_true', default=False, dest='completedoc')
parser.add_argument('-g', '--force-htmlgen', help=
                    'uses HTMLgen even if the html module is available',
                    action='store_true', default=False, dest='forcehtmlgen')

# Process command line arguments.
args = parser.parse_args()

if args.inputfile == '':
    parser.print_help()
    exit(NO_FILE_GIVEN)

if args.outputfile == '':
    args.outputfile = '/dev/stdout'

# Import HTML output modules.
usingHTMLgen = args.forcehtmlgen

if not usingHTMLgen:
    try:
        import html
    except:
        usingHTMLgen = True

if usingHTMLgen:
    try:
        import HTMLgen
    except:
        if args.forcehtmlgen:
            print "Forced to use HTMLgen but couldn't import it.\n\n\
Please install HTMLgen."
        else:
            print "Couldn't import HTMLgen or html.\n\n\
Please install either to use csv2html."
        exit(CANNOT_IMPORT_MODULES)

if usingHTMLgen:
    tg = TableGenHTMLgen(args.title, args.completedoc)
else:
    tg = TableGenHtml(args.title, args.completedoc)

# Read the CSV file and output HTML.
try:
    with open(args.inputfile, 'rb') as incsvfile:
        with open(args.outputfile, 'wb') as outhtmlfile:
            csvreader = csv.reader(incsvfile, dialect='excel',
                                   delimiter=args.delim)
            n = 0  # row number counter
            headerrow = not args.skipheader

            for row in csvreader:
                if headerrow:
                    tg.heading(row)
                    headerrow = False
                else:
                    if n >= args.nstart:
                            if args.renum:
                                row[0] = str(n - args.nstart +
                                             int(args.skipheader or
                                             args.nstart > 0))
                                             # Adds 1 if true to correct for
                                             # numbering rows from zero with no
                                             # zeroth header row or subtracting
                                             # args.nstart.
                            tg.add(row)
                n += 1

            outhtmlfile.write(str(tg))
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    exit(IO_ERROR)
except Exception as e:
    print "Unexpected error:", e
    exit(UNKNOWN_ERROR)

