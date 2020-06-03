// csv2html
// Copyright (c) 2013, 2014, 2017, 2020 D. Bohdan.
// License: BSD (3-clause).  See the file LICENSE.

use snafu::Snafu;

#[derive(Debug, Snafu)]
#[snafu(visibility(pub))]
pub enum Error {
    #[snafu(display("Invalid start row argument: {}", source))]
    CLIStart { source: std::num::ParseIntError },

    #[snafu(display("Invalid delimiter: \"{}\"", delimiter))]
    CLIDelimiter { delimiter: String },

    #[snafu(display(
        "Can not open the input file \"{}\": {}",
        filename,
        source
    ))]
    OpenInput {
        filename: String,
        source: std::io::Error,
    },

    #[snafu(display(
        "Can not open the output file \"{}\": {}",
        filename,
        source
    ))]
    OpenOutput {
        filename: String,
        source: std::io::Error,
    },

    #[snafu(display("Can not parse the CSV header: {}", source))]
    ParseHeader { source: csv::Error },

    #[snafu(display("Can not parse a CSV row: {}", source))]
    ParseRow { source: csv::Error },

    #[snafu(display("Can not write to the output file: {}", source))]
    WriteOutput { source: std::io::Error },
}

pub type Result<T, E = Error> = std::result::Result<T, E>;
