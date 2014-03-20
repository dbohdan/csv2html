csv2html
========

This command line utility and its reusable Python module convert [CSV files](http://en.wikipedia.org/wiki/Comma-separated_values) into HTML tables or complete HTML documents. It can use either the old school `HTMLgen` module or the more modern `html` module to generate its output. The later is preferred since it can produce valid HTML 4.01 Strict. By default csv2html takes the first row of the CSV file to be the [header](http://www.w3schools.com/tags/tag_th.asp) of the HTML table.

You can get the modern Python port of `HTMLgen` from the [GitHub mirror](https://github.com/dbohdan/HTMLgen) or by running `sudo apt-get install python-htmlgen` on Debian and Ubuntu. `html` [is in PyPI](https://pypi.python.org/pypi/html).

Installation
------------

First, make sure Setuptools are installed with

    sudo apt-get install python-setuptools

or

    su -
    yum install python-setuptools

Clone the repository and do

    sudo python setup.py install

This will also install the `html` module.

Command line arguments
----------------------
    usage: csv2html.py [-h] [-o output] [-t TITLE] [-d DELIM] [-s N] [-r] [-n]
                       [-c] [-g]
                       input

    Converts CSV files into HTML tables

    positional arguments:
      input                 input file

    optional arguments:
      -h, --help            show this help message and exit
      -o output, --output output
                            output file
      -t TITLE, --title TITLE
                            document & table title
      -d DELIM, --delimiter DELIM
                            field delimiter for CSV (";" by default)
      -s N, --start N       skip the first N-1 rows, start with row N
      -r, --renumber        replace the first column with row numbers
      -n, --no-header       do not use the first row of the input as the header
      -c, --complete-document
                            output a complete HTML document instead of only the
                            table
      -g, --force-htmlgen   uses HTMLgen even if the html module is available

Use examples
------------

The following takes data from AssetsImportCompleteSample.csv and outputs the corresonding HTML table to test.html:

    ./csv2html.py -o test.html AssetsImportCompleteSample.csv

The example below takes semicolon-delimited data from pub.csv, starting with row 267. The first column of the table is replaced with row numbers starting at 1 (except in the header row, which remains untouched in the output). The output is redirected to the file pub.html.

    ./csv2html.py pub.csv  -d \; -r -s 267 > pub.html

Same as above but this time (due to the option `-c`) the output is a full HTML document instead of just the markup for the table. The option `-g` forces csv2html to produce its HTML output using HTMLgen. The output is then fed to [HTML Tidy](http://tidy.sourceforge.net) (which helps with HTMLgen's upper-case tags) and saved to pub.html.

    ./csv2html.py pub.csv -d \; -r -s 267 -c -g | tidy -q > pub.html

