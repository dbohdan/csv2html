// csv2html
// Copyright (c) 2013-2014, 2017, 2020, 2024 D. Bohdan.
// License: BSD (3-clause). See the file LICENSE.

#![recursion_limit = "1024"]

use std::{
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
    process::exit,
};

use clap::{
    crate_description, crate_name, crate_version, Arg, ArgAction, Command,
};
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
    let matches = Command::new(crate_name!())
        .version(crate_version!())
        .about(crate_description!())
        .arg(
            Arg::new("input")
                .help("Input file")
                .default_value("-")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("OUTPUT")
                .help("Output file")
                .default_value("-")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("title")
                .short('t')
                .long("title")
                .value_name("TITLE")
                .help("HTML document title")
                .default_value("")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("delimiter")
                .short('d')
                .long("delimiter")
                .value_name("DELIM")
                .help("Field delimiter character for CSV (',' by default)")
                .default_value(",")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("start")
                .short('s')
                .long("start")
                .value_name("N")
                .help("Skip the first N-1 rows; start at row N")
                .default_value("0")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("renumber")
                .short('r')
                .long("renumber")
                .help("Replace the first column with row numbers")
                .action(ArgAction::SetTrue),
        )
        .arg(
            Arg::new("no-header")
                .short('n')
                .long("no-header")
                .help("Do not use the first row of the input as the header")
                .action(ArgAction::SetTrue),
        )
        .arg(
            Arg::new("complete-document")
                .short('c')
                .long("complete-document")
                .help("Output a complete HTML document instead of only a table")
                .action(ArgAction::SetTrue),
        )
        .arg(
            Arg::new("table")
                .long("table")
                .value_name("ATTRS")
                .help(
                    "HTML attributes for the tag <table> (e.g., --table \
'foo=\"bar\" baz' results in the output <table \
foo=\"bar\" baz>...</table>); it is up to the \
user to ensure the result is valid HTML",
                )
                .default_value("")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("tr")
                .long("tr")
                .value_name("ATTRS")
                .help("Attributes for <tr>")
                .default_value("")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("th")
                .long("th")
                .value_name("ATTRS")
                .help("Attributes for <th>")
                .default_value("")
                .hide_default_value(true),
        )
        .arg(
            Arg::new("td")
                .long("td")
                .value_name("ATTRS")
                .help("Attributes for <td>")
                .default_value("")
                .hide_default_value(true),
        )
        .get_matches();

    let start_s = matches.get_one::<String>("start").unwrap().to_string();

    let start = start_s.parse::<usize>().context(errors::CLIStartSnafu {})?;

    let delimiter_s = matches.get_one::<String>("delimiter").unwrap();

    ensure!(
        delimiter_s.len() == 1,
        errors::CLIDelimiterSnafu {
            delimiter: delimiter_s
        }
    );

    let delimiter = delimiter_s.bytes().nth(0).unwrap();

    Ok(Opts {
        input: matches.get_one::<String>("input").unwrap().to_string(),
        output: matches.get_one::<String>("output").unwrap().to_string(),
        start: start,
        delimiter: delimiter,
        title: matches.get_one::<String>("title").unwrap().to_string(),
        renumber: matches.get_flag("renumber"),
        header: !matches.get_flag("no-header"),
        complete_document: matches.get_flag("complete-document"),
        table_attrs: matches.get_one::<String>("table").unwrap().to_string(),
        tr_attrs: matches.get_one::<String>("tr").unwrap().to_string(),
        th_attrs: matches.get_one::<String>("th").unwrap().to_string(),
        td_attrs: matches.get_one::<String>("td").unwrap().to_string(),
    })
}

fn app() -> errors::Result<()> {
    let opts = cli()?;

    let input: Box<dyn BufRead> = if &opts.input == "-" {
        Box::new(BufReader::new(std::io::stdin()))
    } else {
        Box::new(BufReader::new(File::open(&opts.input).context(
            errors::OpenInputSnafu {
                filename: &opts.input,
            },
        )?))
    };

    let mut output: Box<dyn Write> = if &opts.output == "-" {
        Box::new(BufWriter::new(std::io::stdout()))
    } else {
        Box::new(BufWriter::new(File::create(&opts.output).context(
            errors::OpenOutputSnafu {
                filename: &opts.output,
            },
        )?))
    };

    write!(
        output,
        "{}",
        tablegen::start(opts.complete_document, &opts.title, &opts.table_attrs)
    )
    .context(errors::WriteOutputSnafu {})?;

    let mut csv_reader = ReaderBuilder::new()
        .flexible(true)
        .has_headers(opts.header)
        .delimiter(opts.delimiter)
        .from_reader(input);

    if opts.header {
        let headers = csv_reader
            .headers()
            .context(errors::ParseHeaderSnafu {})?
            .iter()
            .collect::<Vec<_>>();

        write!(
            output,
            "{}",
            tablegen::row(&headers, true, &opts.tr_attrs, &opts.th_attrs)
        )
        .context(errors::WriteOutputSnafu {})?;
    }

    let mut i: u64 = 1;
    let mut skip = opts.start;
    if skip > 0 && opts.header {
        skip -= 1;
    }

    for result in csv_reader.records().skip(skip) {
        let record = result.context(errors::ParseRowSnafu {})?;
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
        .context(errors::WriteOutputSnafu {})?;

        i += 1;
    }

    write!(output, "{}", tablegen::end(opts.complete_document))
        .context(errors::WriteOutputSnafu {})?;

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
