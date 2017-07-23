# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD-3. See the file LICENSE.
import sys
if sys.version_info >= (3, 2):
    from html import escape
else:
    from cgi import escape


def _tag_with_attrs(tag, attrs):
    tag_attrs = attrs.get(tag, '')
    return '<' + tag + ('' if tag_attrs == '' else ' ' + tag_attrs) + '>'


def start(completedoc=False, title='', attrs={}):
    s = ''
    if completedoc:
        s += ('<!DOCTYPE html>\n<html>\n<head><title>' + escape(title) +
              '</title></head>\n<body>')
    s += _tag_with_attrs('table', attrs) + '\n'
    return s


def end(completedoc=False):
    s = '</table>'
    if completedoc:
        s += '</body>\n</html>'
    return s


def row(r, headerrow=False, attrs={}):
    if headerrow:
        tag = 'th'
    else:
        tag = 'td'

    res = [_tag_with_attrs('tr', attrs)]
    for cell in r:
        res.append(_tag_with_attrs(tag, attrs) + escape(cell) +
                   '</' + tag + '>')
    res.append('</tr>\n')

    return ''.join(res)
