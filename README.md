csv2html
========

Converts CSV tables into HTML tables using old school HTMLgen or the html module found at https://pypi.python.org/pypi/html.


Usage
-----
    usage: csv2html.py [-h] [-o OUTPUTFILE] [-t TITLE] [-d DELIM] [-s N] [-r]
                       inputfile
    
    Converts CSV tables into HTML tables
    
    positional arguments:
      inputfile             input file
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUTFILE, --output OUTPUTFILE
                            output file
      -t TITLE, --title TITLE
                            document & table title
      -d DELIM, --delimiter DELIM
                            field delimiter for CSV
      -s N, --start N       skip the first N-1 rows, start with row N
      -r, --renumber        replace the first column with row numbers
