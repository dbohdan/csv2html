# csv2html

This command line utility converts [CSV files](http://en.wikipedia.org/wiki/Comma-separated_values) to HTML tables and complete HTML documents. It requires Rust 1.43 or later to build and Python 3.5 or later to test. By default it uses the first row of the CSV file as the [header](https://developer.mozilla.org/en/docs/Web/HTML/Element/th) of the HTML table.

The older Python version is preserved in the branch [`python`](https://github.com/dbohdan/csv2html/tree/python).


## Installation

Prebuilt Linux and Windows binaries are available. They are attached to releases on the [Releases](https://github.com/dbohdan/csv2html/releases) page.

### Installing with Cargo

```shell
cargo install csv2html
```

### Building on Debian and Ubuntu

Follow the instructions to build a static Linux binary of `csv2html` from source on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/). Through Rustup add the stable MUSL target for your CPU.

```sh
rustup target add x86_64-unknown-linux-musl
```

2\. Install the build and testing dependencies.

```sh
sudo apt install build-essential musl-tools python3
```

3\. Clone this repository. Build the binary.

    git clone https://github.com/dbohdan/csv2html
    cd csv2html
    make test
    make release-linux

### Cross-compiling for Windows

Follow the instructions to build a 32-bit Windows binary of `csv2html` on recent Debian and Ubuntu.

1\. Install [Rustup](https://rustup.rs/). Through Rustup add the i686 GNU ABI Windows target.

```sh
rustup target add i686-pc-windows-gnu
```

2\. Install the build dependencies.

```sh
sudo apt install build-essential mingw-w64
```

3\. Configure Cargo for cross-compilation. Put the following in `~/.cargo/config`.

```toml
[target.i686-pc-windows-gnu]
linker = "/usr/bin/i686-w64-mingw32-gcc"
```

4\. Clone this repository. Build the binary.

    git clone https://github.com/dbohdan/csv2html
    cd csv2html
    make release-windows


## Command line arguments

```none
Convert CSV files to HTML tables

Usage: csv2html [OPTIONS] [input]

Arguments:
  [input]  Input file

Options:
  -o, --output <OUTPUT>    Output file
  -t, --title <TITLE>      HTML document title
  -d, --delimiter <DELIM>  Field delimiter character for CSV (',' by default)
  -s, --start <N>          Skip the first N-1 rows; start at row N
  -r, --renumber           Replace the first column with row numbers
  -n, --no-header          Do not use the first row of the input as the header
  -c, --complete-document  Output a complete HTML document instead of only a table
      --table <ATTRS>      HTML attributes for the tag <table> (e.g., --table 'foo="bar" baz' results in the output <table foo="bar" baz>...</table>); it is up to the user to ensure the result is valid HTML
      --tr <ATTRS>         Attributes for <tr>
      --th <ATTRS>         Attributes for <th>
      --td <ATTRS>         Attributes for <td>
  -h, --help               Print help
  -V, --version            Print version
```


## Use examples

The following command reads the data from `test/test.csv` and writes the corresponding HTML table to `test.html`:

    csv2html -o test.html tests/test.csv

The next command takes semicolon-delimited data from `pub.csv`, starting with row 267. The first column of the table is replaced with the row number starting at 1 (except in the header row, which is untouched). The output is redirected to the file `pub.html`.

    csv2html pub.csv -d \; -r -s 267 > pub.html

Same as above, but this time the output is a full HTML document instead of just the markup for the table:

    csv2html pub.csv -d \; -r -s 267 -c > pub.html

If the input file is tab-delimited, use `\t` as the deliminter argument.

    csv2html --delimiter '\t' tests/test.tsv

    csv2html-win32.exe --delimiter \t tests/test.tsv

`\t` is the only [backslash escape sequence](https://en.wikipedia.org/wiki/Escape_sequences_in_C) that is implemented.

## License

Three-clause ("new" or "revised") BSD. See the file `LICENSE`.
