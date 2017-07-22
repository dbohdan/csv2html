# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD-3. See the file LICENSE.
import cgi

def start(completedoc=False, title=""):
    s = ""
    if completedoc:
        s += ("<!DOCTYPE html>\n<html>\n<head><title>" + title +
                "</title><html><body>")
    s += '<table border="1">\n'
    return s

def end(completedoc=False):
    s = "</table>"
    if completedoc:
        s += "</body>\n</html>"
    return s

def row(r, headerrow=False):
    if headerrow:
        tag = "th"
    else:
        tag = "td"

    res = ["<tr>"]
    for cell in r:
        res.append("<" + tag + ">" + cgi.escape(cell) + "</" + tag + ">")
    res.append("</tr>\n")

    return "".join(res)
