# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD-3. See the file LICENSE.
import sys
if sys.version_info >= (3, 2):
    from html import escape
else:
    from cgi import escape


def start(completedoc=False, title=''):
    s = ''
    if completedoc:
        s += ('<!DOCTYPE html>\n<html>\n<head><title>' + escape(title) +
              '</title></head>\n<body>')
    s += '<table>\n'
    return s


def end(completedoc=False):
    s = '</table>'
    if completedoc:
        s += '</body>\n</html>'
    return s


def row(r, headerrow=False):
    if headerrow:
        tag = 'th'
    else:
        tag = 'td'

    res = ['<tr>']
    for cell in r:
        res.append('<' + tag + '>' + escape(cell) + '</' + tag + '>')
    res.append('</tr>\n')

    return ''.join(res)
