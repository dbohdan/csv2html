#!/usr/bin/env python
# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD-3. See the file LICENSE.
'''
This module converts CSV files to HTML tables. It can be used as a standalone
program.
'''

from __future__ import print_function

from . import __version__
from . import tablegen

import argparse
import csv
import os
import sys

DEFAULT_DELIMITER = ','
PYTHON2 = sys.version_info[0] == 2


def convert_csv_to_html(inputstream, outputstream, title='',
                        delim=DEFAULT_DELIMITER, nstart=0, skipheader=False,
                        renum=False, completedoc=False):
    '''
    Takes CSV data from inputstream (an iterable) and outputs an HTML table to
    outputstream (anything with a write method that takes a string).
    '''

    # Read the CSV stream.
    csvreader = csv.reader(inputstream, dialect='excel',
                           delimiter=delim)
    nrow = 0  # The row number counter.

    if sys.version_info[0] == 2:
        def next_row():
            return csvreader.next()
    else:
        def next_row():
            return csvreader.__next__()

    outputstream.write(tablegen.start(completedoc, title))
    if not skipheader:
        row = next_row()
        outputstream.write(tablegen.row(row, True))
        nrow += 1
    while nrow < nstart:
        next_row()
        nrow += 1
    for row in csvreader:
        if renum:
            # If there is no zeroth header row, add 1 to the new row number
            # to correct for the rows being counted from zero. Do the same if
            # we're counting from nstart.
            row[0] = str(nrow - nstart + int(skipheader or nstart > 0))
        outputstream.write(tablegen.row(row))
        nrow += 1
    outputstream.write(tablegen.end(completedoc))


def main():
    '''
    This function is called when the module is run as the main program.
    It handles command line options and opening files for convert_csv_to_html.
    '''

    # The sendmail exit codes are convenient for scripting, but they are
    # unavailable on Windows. We hard code them here as a backup for that case.
    # The numbers come from the POSIX sysexit.h.
    exit_codes = {'EX_OK': 0,
                  'EX_NOINPUT': 66,
                  'EX_UNAVAILABLE': 69,
                  'EX_SOFTWARE': 70,
                  'EX_IOERR': 74}

    # Replace the hard coded numerical values of the exit codes with those from
    # the module `os` if it has them. Unless your system is quite strange they
    # shouldn't actually differ from the above.
    for code in exit_codes:
        if hasattr(os, code):
            exit_codes[code] = getattr(os, code)

    # Configure the command line argument parser.
    parser = argparse.ArgumentParser(description='Convert CSV files to \
                                     HTML tables')
    parser.add_argument('inputfile', help='input file',
                        default='', metavar='input')
    parser.add_argument('-o', '--output', help='output file',
                        default='', required=False, metavar='output',
                        dest='outputfile')
    parser.add_argument('-t', '--title', help='document & table title',
                        default='')
    parser.add_argument('-d', '--delimiter', help='field delimiter for CSV \
                        ("%s" by default)' % DEFAULT_DELIMITER,
                        default=DEFAULT_DELIMITER,
                        dest='delim')
    parser.add_argument('-s', '--start', metavar='N',
                        help='skip the first N-1 rows, start with row N',
                        type=int, default=0, dest='nstart')
    parser.add_argument('-r', '--renumber',
                        help='replace the first column with row numbers',
                        action='store_true', default=False, dest='renum')
    parser.add_argument('-n', '--no-header', help='do not use the first row of \
                        the input as the header',
                        action='store_true', default=False, dest='skipheader')
    parser.add_argument('-c', '--complete-document', help='output a complete \
                        HTML document instead of only a table',
                        action='store_true', default=False, dest='completedoc')
    parser.add_argument('-v', '--version',
                        action='version', version=__version__)

    # Process the command line arguments.
    args = parser.parse_args()

    if args.inputfile == '':
        parser.print_help()
        sys.exit(exit_codes['EX_NOINPUT'])

    try:
        with open(args.inputfile, 'rb' if PYTHON2 else 'r') as incsvfile:
            # Only write to stdout if the output file name is empty. If the
            # output file can't be written to, it is instead handled as an
            # exception.
            if args.outputfile != '':
                outhtmlfile = open(args.outputfile, 'wb' if PYTHON2 else 'w')
            else:
                outhtmlfile = sys.stdout

            convert_csv_to_html(incsvfile, outhtmlfile, args.title,
                                args.delim, args.nstart, args.skipheader,
                                args.renum, args.completedoc)

            outhtmlfile.close()
        sys.exit(exit_codes['EX_OK'])
    except IOError as e:
        print('I/O error({0}): {1}'.format(e.errno, e.strerror),
              file=sys.stderr)
        sys.exit(exit_codes['EX_IOERR'])
    except Exception as e:
        print('Unexpected error:', e, file=sys.stderr)
        sys.exit(exit_codes['EX_SOFTWARE'])


if __name__ == '__main__':
    main()
