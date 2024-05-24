// Integration tests for csv2html.
// Copyright (c) 2013-2014, 2017, 2020, 2021, 2024 D. Bohdan.
// License: BSD (3-clause). See the file LICENSE.

use std::{
    convert::AsRef,
    env,
    ffi::OsStr,
    fs,
    io::{Result, Write},
    iter::IntoIterator,
    process::{Command, Stdio},
};
use {exitcode, regex::Regex};

#[derive(Debug, Eq, PartialEq)]
struct Output {
    code: i32,
    stderr: String,
    stdout: String,
}

fn csv2html_cmd() -> String {
    env::var("CSV2HTML_COMMAND")
        .expect("Environment variable CSV2HTML_COMMAND should be set")
}

fn csv2html<I, S>(args: I) -> Result<Output>
where
    I: IntoIterator<Item = S>,
    S: AsRef<OsStr>,
{
    let output = Command::new(csv2html_cmd()).args(args).output()?;

    Ok(Output {
        code: output.status.code().unwrap(),
        stderr: String::from_utf8(output.stderr).unwrap(),
        stdout: String::from_utf8(output.stdout).unwrap(),
    })
}

fn read_file<S>(filename: S) -> Result<String>
where
    S: AsRef<str> + std::fmt::Display,
{
    fs::read_to_string(format!("tests/{}", filename))
}

#[test]
#[ignore]
fn help_message() {
    let re = Regex::new(r"Convert CSV files to HTML tables").unwrap();

    let output = csv2html(&["-h"]).unwrap();
    assert!(re.is_match(&output.stdout));
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn version() {
    let re = Regex::new(r"\d+\.\d+\.\d+\s*$").unwrap();

    let output = csv2html(&["--version"]).unwrap();
    assert!(re.is_match(&output.stdout));
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn default() {
    let output = csv2html(&["tests/test.csv"]).unwrap();
    let reference = read_file("test-default.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn tab_escape() {
    let output = csv2html(&["--delimiter", "\\t", "tests/test.tsv"]).unwrap();
    let reference = read_file("test-default.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn tab_literal() {
    let output = csv2html(&["--delimiter", "\t", "tests/test.tsv"]).unwrap();
    let reference = read_file("test-default.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn stdin() {
    let input = read_file("test.csv").unwrap();
    let reference = read_file("test-default.html").unwrap();

    let mut proc = Command::new(csv2html_cmd())
        .args(&["-"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();

    let _ = proc.stdin.take().unwrap().write_all(input.as_bytes());
    let output = proc.wait_with_output().unwrap();

    assert_eq!(String::from_utf8(output.stdout).unwrap(), reference);
    assert_eq!(output.status.code().unwrap(), exitcode::OK);
}

#[test]
#[ignore]
fn complete_doc_and_title() {
    let output = csv2html(&[
        "--title",
        "Foo & Bar",
        "--complete-document",
        "tests/test.csv",
    ])
    .unwrap();
    let reference = read_file("test-c-t.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn renum() {
    let output = csv2html(&["--renumber", "tests/test.csv"]).unwrap();
    let reference = read_file("test-r.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn no_header() {
    let output = csv2html(&["-n", "tests/test.csv"]).unwrap();
    let reference = read_file("test-n.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn start_5() {
    let output = csv2html(&["--start", "5", "tests/test.csv"]).unwrap();
    let reference = read_file("test-s5.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn start_0_and_no_header() {
    let output =
        csv2html(&["--start", "0", "--no-header", "tests/test.csv"]).unwrap();
    let reference = read_file("test-s0-n.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn start_1_and_no_header() {
    let output =
        csv2html(&["--start", "1", "--no-header", "tests/test.csv"]).unwrap();
    let reference = read_file("test-s1-n.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn start_2_and_no_header() {
    let output =
        csv2html(&["--start", "2", "--no-header", "tests/test.csv"]).unwrap();
    let reference = read_file("test-s2-n.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn start_5_and_no_header() {
    let output =
        csv2html(&["--start", "5", "--no-header", "tests/test.csv"]).unwrap();
    let reference = read_file("test-s5-n.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn attrs() {
    let output = csv2html(&[
        "--table",
        "class=\"foo\" id=\"bar\"",
        "--tr",
        "class=\"row\"",
        "--th",
        "class=\"hcell\"",
        "--td",
        "class=\"cell\"",
        "tests/test.csv",
    ])
    .unwrap();
    let reference = read_file("test-attrs.html").unwrap();

    assert_eq!(output.stdout, reference);
    assert_eq!(output.code, exitcode::OK);
}

#[test]
#[ignore]
fn no_file() {
    let re = Regex::new(r".*Can not open the input file.*").unwrap();

    let output = csv2html(&["tests/does-not-exist.csv"]).unwrap();
    assert!(re.is_match(&output.stderr));
    assert_eq!(output.code, exitcode::IOERR);
}

#[test]
#[ignore]
fn garbage_file() {
    let re = Regex::new(r".*Can not parse.*").unwrap();

    let output = csv2html(&["tests/garbage"]).unwrap();
    assert!(re.is_match(&output.stderr));
    assert_eq!(output.code, exitcode::DATAERR);
}
