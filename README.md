# csv2html

[![Travis CI Build Status](https://travis-ci.org/dbohdan/csv2html.svg?branch=master)](https://travis-ci.org/dbohdan/csv2html)
[![AppVeyor CI Build Status](https://ci.appveyor.com/api/projects/status/github/dbohdan/csv2html?branch=master&svg=true)](https://ci.appveyor.com/project/dbohdan/csv2html)

This command line utility converts [CSV files](http://en.wikipedia.org/wiki/Comma-separated_values) to HTML tables and complete HTML documents.  It requires Rust 1.43 or later to build and Python 3.5 or later to test.  By default it uses the first row of the CSV file as the [header](https://developer.mozilla.org/en/docs/Web/HTML/Element/th) of the HTML table.

The older Python version is preserved in the branch [`python`](https://github.com/dbohdan/csv2html/tree/python).


## Installation

Prebuilt Linux and Windows binaries are available.  They are attached to releases on the [Releases](https://github.com/dbohdan/csv2html/releases) page.

### Building on Debian and Ubuntu

Follow the instructions to build a static Linux binary of `csv2html` from source on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/).  Through Rustup add the stable MUSL target for your CPU.

```sh
rustup target add x86_64-unknown-linux-musl
```

2\. Install the build and testing dependencies.

```sh
sudo apt install build-essential musl-tools python3
```

3\. Clone this repository.  Build and install the binary.

    git clone https://github.com/dbohdan/csv2html
    cd csv2html
    make test
    make release
    sudo make install "BUILD_USER=$USER"

### Cross-compiling for Windows

Follow the instructions to build a 32-bit Windows binary of `csv2html` on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/).  Through Rustup add the i686 GNU ABI Windows target.

```sh
rustup target add i686-pc-windows-gnu
```

2\. Install the build dependencies.

```sh
sudo apt install build-essential mingw-w64
```

3\. Configure Cargo for cross-compilation.  Put the following in `~/.cargo/config`.

```toml
[target.i686-pc-windows-gnu]
linker = "/usr/bin/i686-w64-mingw32-gcc"
```

4\. Clone this repository.  Build the binary.

    git clone https://github.com/dbohdan/csv2html
    cd csv2html
    make release TARGET=i686-pc-windows-gnu
    cp "/tmp/$USER/csv2html-rust/i686-pc-windows-gnu/release/csv2html.exe" .


## Command line arguments

```none
csv2html 3.0.0
Convert CSV files to HTML tables

USAGE:
    csv2html [FLAGS] [OPTIONS] [input]

FLAGS:
    -c, --complete-document    Output a complete HTML document instead of only a
                               table
    -h, --help                 Prints help information
    -n, --no-header            Do not use the first row of the input as the
                               header
    -r, --renumber             Replace the first column with row numbers
    -V, --version              Prints version information

OPTIONS:
    -d, --delimiter <DELIM>    Field delimiter character for CSV (',' by
                               default)
    -o, --output <OUTPUT>      Output file
    -s, --start <N>            Skip the first N-1 rows; start at row N
        --table <ATTRS>        HTML attributes for the tag <table> (e.g.,
                               --table 'foo="bar" baz' results in the output
                               <table foo="bar" baz>...</table>); it is up to
                               the user to ensure the result is valid HTML
        --td <ATTRS>           Attributes for <td>
        --th <ATTRS>           Attributes for <th>
    -t, --title <TITLE>        HTML document title
        --tr <ATTRS>           Attributes for <tr>

ARGS:
    <input>    Input file
```


## Use examples

The following command reads the data from `test/test.csv` and writes the corresponding HTML table to `test.html`:

    csv2html -o test.html test/test.csv

The example below takes semicolon-delimited data from `pub.csv`, starting with row 267. The first column of the table is replaced with the row numbers starting at 1 (except in the header row). The output is redirected to the file `pub.html`.

    csv2html pub.csv -d \; -r -s 267 > pub.html

Same as above, but this time the output is a full HTML document instead of just the markup for the table:

    csv2html pub.csv -d \; -r -s 267 -c > pub.html


## License

Three-clause ("new" or "revised") BSD.  See the file license.
