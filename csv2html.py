#!/usr/bin/env python
# This software converts CSV tables into HTML tables.
# For best results install https://pypi.python.org/pypi/html.
# See the files README.md and LICENSE for more information.
# -- dbohdan 2013.03.22


import csv
import os
import sys
import argparse


try:
    import html
    using_htmlgen = False
except:
    import HTMLgen
    using_htmlgen = True


class tablegen(object):
    def __init__(self, title=''):
        pass

    def __str__(self):

        pass

    def heading(self, h):
        pass

    def add(self, row):
        pass


class tablegen1(tablegen):
    """HTMLgen-based table generator."""

    def __init__(self, title=""):
        self.t = HTMLgen.Table(title)
        self.t.body = []

    def __str__(self):
        return str(self.t)

    def heading(self, h):
        self.t.heading = row

    def add(self, row):
        self.t.body.append([x if x != '' else '&nbsp;' for x in row])


class tablegen2(tablegen):
    """html unit-based table generator."""

    def __init__(self, title=''):
        self.h = html.HTML()
        self.t = self.h.table(border='1')

    def __str__(self):
        return str(self.h)

    def heading(self, h):
        r = self.t.tr
        for item in row:
            if item != '':
                r.th(item)
            else:
                t = r.th
                t.text('&nbsp;', escape=False)

    def add(self, row):
        r = self.t.tr
        for item in row:
            if item != '':
                r.td(item)
            else:
                t = r.td
                t.text('&nbsp;', escape=False)


parser = argparse.ArgumentParser(description=
                                 'Converts CSV tables into HTML tables')
parser.add_argument('inputfile', help='input file',
                    default='', metavar='input')
parser.add_argument('-o', '--output', help='output file',
                    default='', required=False, metavar='output',
                    dest='outputfile')
parser.add_argument('-t', '--title', help='document & table title',
                    default='')
parser.add_argument('-d', '--delimiter', help='field delimiter for CSV',
                    default=';', dest='delim')
parser.add_argument('-s', '--start', metavar='N', help=
                    'skip the first N-1 rows, start with row N',
                    type=int, default=0, dest='nstart')
parser.add_argument('-r', '--renumber', help=
                    'replace the first column with row numbers',
                    action='store_true', dest='renum')

args = parser.parse_args()

if args.inputfile == '':
    parser.print_help()
    exit(1)

if args.outputfile == '':
    args.outputfile = '/dev/stdout'

if using_htmlgen:
    tg = tablegen1(args.title)
else:
    tg = tablegen2(args.title)


try:
    with open(args.inputfile, 'rb') as incsvfile:
        with open(args.outputfile, 'wb') as outhtmlfile:
            csvreader = csv.reader(incsvfile, dialect='excel',
                                   delimiter=args.delim)
            n = 0  # row number counter

            for row in csvreader:
                if n == 0:
                    tg.heading(row)
                else:
                    if n > args.nstart:
                            if args.renum:
                                row[0] = str(n - args.nstart)
                            tg.add(row)
                n += 1

            outhtmlfile.write(str(tg))
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    exit(2)
except Exception as e:
    print "Unexpected error:", e
    exit(127)

