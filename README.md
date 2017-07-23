csv2html
========

[![Travis CI Build Status](https://travis-ci.org/dbohdan/csv2html.svg?branch=master)](https://travis-ci.org/dbohdan/csv2html)
[![AppVeyor CI Build Status](https://ci.appveyor.com/api/projects/status/github/dbohdan/csv2html?branch=master&svg=true)](https://ci.appveyor.com/project/dbohdan/csv2html)

This command line utility and reusable Python package converts [CSV files](http://en.wikipedia.org/wiki/Comma-separated_values) to HTML tables or complete HTML documents. It requires Python 2.7 or Python 3.2 or later. By default it uses the first row of the CSV file as the [header](https://developer.mozilla.org/en/docs/Web/HTML/Element/th) of the HTML table.


Installation
------------

First, make sure Setuptools are installed with

    sudo apt-get install python-setuptools  # Debian/Ubuntu

or

    su -
    dnf install python-setuptools  # Fedora/CentOS

Clone the repository and run

    sudo python setup.py install


Command line arguments
----------------------

    usage: csv2html [-h] [-o output] [-t TITLE] [-d DELIM] [-s N] [-r] [-n] [-c]
                    [-v] [--table ATTRS] [--tr ATTRS] [--th ATTRS] [--td ATTRS]
                    input

    Convert CSV files to HTML tables

    positional arguments:
      input                 input file

    optional arguments:
      -h, --help            show this help message and exit
      -o output, --output output
                            output file
      -t TITLE, --title TITLE
                            HTML document title
      -d DELIM, --delimiter DELIM
                            field delimiter for CSV ("," by default)
      -s N, --start N       skip the first N-1 rows, start at row N
      -r, --renumber        replace the first column with row numbers
      -n, --no-header       do not use the first row of the input as the header
      -c, --complete-document
                            output a complete HTML document instead of only a
                            table
      -v, --version         show program's version number and exit

    HTML tag attributes:
      --table ATTRS         Attributes for the tag <table> (e.g., --table
                            'foo="bar" baz' results in the output <table foo="bar"
                            baz>...</table>); it is up to the user to ensure the
                            result is valid HTML
      --tr ATTRS            Attributes for <tr>
      --th ATTRS            Attributes for <th>
      --td ATTRS            Attributes for <td>


Use examples
------------

The following command reads the data from `test/test.csv` and writes the corresponding HTML table to `test.html`:

    csv2html -o test.html test/test.csv

The example below takes semicolon-delimited data from `pub.csv`, starting with row 267. The first column of the table is replaced with the row numbers starting at 1 (except in the header row). The output is redirected to the file `pub.html`.

    csv2html pub.csv -d \; -r -s 267 > pub.html

Same as above, but this time the output is a full HTML document instead of just the markup for the table:

    csv2html pub.csv -d \; -r -s 267 -c > pub.html
