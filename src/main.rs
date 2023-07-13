// csv2html
// Copyright (c) 2013, 2014, 2017, 2020 D. Bohdan.
// License: BSD (3-clause). See the file LICENSE.

#![recursion_limit = "1024"]

use std::{
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
    process::exit,
};

use clap::{App, Arg};
use csv::ReaderBuilder;
use exitcode;
use snafu::{ensure, ResultExt};

use csv2html::{errors, tablegen};

#[derive(Debug)]
struct Opts {
    input: String,
    output: String,
    title: String,
    delimiter: u8,
    start: usize,
    renumber: bool,
    header: bool,
    complete_document: bool,
    table_attrs: String,
    th_attrs: String,
    tr_attrs: String,
    td_attrs: String,
}

fn cli() -> errors::Result<Opts> {
    let matches = App::new("csv2html")
        .version("3.0.1")
        .about("Convert CSV files to HTML tables")
        .arg(Arg::with_name("input").help("Input file").index(1))
        .arg(
            Arg::with_name("output")
                .short("o")
                .long("output")
                .value_name("OUTPUT")
                .help("Output file"),
        )
        .arg(
            Arg::with_name("title")
                .short("t")
                .long("title")
                .value_name("TITLE")
                .help("HTML document title"),
        )
        .arg(
            Arg::with_name("delimiter")
                .short("d")
                .long("delimiter")
                .value_name("DELIM")
                .help("Field delimiter character for CSV (',' by default)"),
        )
        .arg(
            Arg::with_name("start")
                .short("s")
                .long("start")
                .value_name("N")
                .help("Skip the first N-1 rows; start at row N"),
        )
        .arg(
            Arg::with_name("renumber")
                .short("r")
                .long("renumber")
                .help("Replace the first column with row numbers"),
        )
        .arg(
            Arg::with_name("no-header")
                .short("n")
                .long("no-header")
                .help("Do not use the first row of the input as the header"),
        )
        .arg(
            Arg::with_name("complete-document")
                .short("c")
                .long("complete-document")
                .help(
                    "Output a complete HTML document instead of only a table",
                ),
        )
        .arg(
            Arg::with_name("table")
                .long("table")
                .value_name("ATTRS")
                .help(
                    "HTML attributes for the tag <table> (e.g., --table \
'foo=\"bar\" baz' results in the output <table \
foo=\"bar\" baz>...</table>); it is up to the \
user to ensure the result is valid HTML",
                ),
        )
        .arg(
            Arg::with_name("tr")
                .long("tr")
                .value_name("ATTRS")
                .help("Attributes for <tr>"),
        )
        .arg(
            Arg::with_name("th")
                .long("th")
                .value_name("ATTRS")
                .help("Attributes for <th>"),
        )
        .arg(
            Arg::with_name("td")
                .long("td")
                .value_name("ATTRS")
                .help("Attributes for <td>"),
        )
        .get_matches();

    let input = matches.value_of("input").unwrap_or("-").to_string();

    let output = matches.value_of("output").unwrap_or("-").to_string();

    let start_s = matches.value_of("start").unwrap_or("0");
    let start = start_s.parse::<usize>().context(errors::CLIStart {})?;

    let delimiter_s = matches.value_of("delimiter").unwrap_or(",");
    ensure!(
        delimiter_s.len() == 1,
        errors::CLIDelimiter {
            delimiter: delimiter_s
        }
    );

    let delimiter = delimiter_s.bytes().nth(0).unwrap();

    let title = matches.value_of("title").unwrap_or("").to_string();

    Ok(Opts {
        input: input,
        output: output,
        start: start,
        delimiter: delimiter,
        title: title,
        renumber: matches.is_present("renumber"),
        header: !matches.is_present("no-header"),
        complete_document: matches.is_present("complete-document"),
        table_attrs: matches.value_of("table").unwrap_or("").to_string(),
        tr_attrs: matches.value_of("tr").unwrap_or("").to_string(),
        th_attrs: matches.value_of("th").unwrap_or("").to_string(),
        td_attrs: matches.value_of("td").unwrap_or("").to_string(),
    })
}

fn app() -> errors::Result<()> {
    let opts = cli()?;

    let input: Box<dyn BufRead> = if &opts.input == "-" {
        Box::new(BufReader::new(std::io::stdin()))
    } else {
        Box::new(BufReader::new(File::open(&opts.input).context(
            errors::OpenInput {
                filename: &opts.input,
            },
        )?))
    };

    let mut output: Box<dyn Write> = if &opts.output == "-" {
        Box::new(BufWriter::new(std::io::stdout()))
    } else {
        Box::new(BufWriter::new(File::create(&opts.output).context(
            errors::OpenOutput {
                filename: &opts.output,
            },
        )?))
    };

    write!(
        output,
        "{}",
        tablegen::start(opts.complete_document, &opts.title, &opts.table_attrs)
    )
    .context(errors::WriteOutput {})?;

    let mut csv_reader = ReaderBuilder::new()
        .flexible(true)
        .has_headers(opts.header)
        .delimiter(opts.delimiter)
        .from_reader(input);

    if opts.header {
        let headers = csv_reader
            .headers()
            .context(errors::ParseHeader {})?
            .iter()
            .collect::<Vec<_>>();

        write!(
            output,
            "{}",
            tablegen::row(&headers, true, &opts.tr_attrs, &opts.th_attrs)
        )
        .context(errors::WriteOutput {})?;
    }

    let mut i: u64 = 1;
    let mut skip = opts.start;
    if skip > 0 && opts.header {
        skip -= 1;
    }

    for result in csv_reader.records().skip(skip) {
        let record = result.context(errors::ParseRow {})?;
        let mut row = record.iter().collect::<Vec<_>>();

        let i_s = i.to_string();

        if opts.renumber {
            row[0] = &i_s;
        }

        write!(
            output,
            "{}",
            tablegen::row(&row, false, &opts.tr_attrs, &opts.td_attrs)
        )
        .context(errors::WriteOutput {})?;

        i += 1;
    }

    write!(output, "{}", tablegen::end(opts.complete_document))
        .context(errors::WriteOutput {})?;

    Ok(())
}

fn main() {
    match app() {
        Ok(_) => exit(exitcode::OK),
        Err(ref err) => match err {
            errors::Error::OpenInput {
                filename: _,
                source: _,
            }
            | errors::Error::OpenOutput {
                filename: _,
                source: _,
            }
            | errors::Error::WriteOutput { source: _ } => {
                eprintln!("{}", err);
                exit(exitcode::IOERR);
            }
            errors::Error::ParseHeader { source: _ }
            | errors::Error::ParseRow { source: _ } => {
                eprintln!("{}", err);
                exit(exitcode::DATAERR);
            }
            _ => {
                eprintln!("{}", err);
                exit(exitcode::SOFTWARE);
            }
        },
    }
}
