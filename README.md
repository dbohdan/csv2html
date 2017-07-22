csv2html
========

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
                    [-v]
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


Use examples
------------

The following command takes data from `test/test.csv` and outputs the corresponding HTML table to `test.html`:

    csv2html -o test.html test/test.csv

The example below takes semicolon-delimited data from `pub.csv`, starting with row 267. The first column of the table is replaced with the row numbers starting at 1 (except in the header row). The output is redirected to the file `pub.html`.

    csv2html pub.csv -d \; -r -s 267 > pub.html

Same as above, but this time the output is a full HTML document instead of just the markup for the table:

    csv2html pub.csv -d \; -r -s 267 -c > pub.html
