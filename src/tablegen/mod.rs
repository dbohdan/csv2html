// csv2html
// Copyright (c) 2013, 2014, 2017, 2020 D. Bohdan.
// License: BSD (3-clause).  See the file LICENSE.

pub fn escape(s: &str) -> String {
    s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
}

fn tag_with_attrs(tag: &str, attrs: &str) -> String {
    if attrs == "" {
        format!("<{}>", tag)
    } else {
        format!("<{} {}>", tag, attrs)
    }
}

pub fn start(complete_doc: bool, title: &str, table_attrs: &str) -> String {
    let mut s = String::new();

    if complete_doc {
        s.push_str(&format!(
            "<!DOCTYPE html>\n<html>\n<head><title>{}</title></head>\n<body>\n",
            escape(title),
        ));
    }

    s.push_str(&tag_with_attrs("table", table_attrs));
    s.push('\n');

    s
}

pub fn end(complete_doc: bool) -> String {
    let mut s = "</table>\n".to_string();

    if complete_doc {
        s.push_str("</body>\n</html>\n");
    }

    s
}

pub fn row(
    cols: &[&str],
    header: bool,
    row_attrs: &str,
    col_attrs: &str,
) -> String {
    let col_tag = if header { "th" } else { "td" };

    let mut s = String::new();

    s.push_str(&tag_with_attrs("tr", row_attrs));

    for col in cols {
        s.push_str(&format!(
            "{}{}</{}>",
            &tag_with_attrs(col_tag, col_attrs),
            &escape(col),
            &col_tag
        ));
    }

    s.push_str("</tr>\n");

    s
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_start_1() {
        assert_eq!(start(false, "<\"Greetings!\">", "x=y"), "<table x=y>\n");
    }

    #[test]
    fn test_start_2() {
        assert_eq!(
            start(true, "<\"Greetings!\">", ""),
            "<!DOCTYPE html>\n<html>\n<head><title>&lt;&quot;\
            Greetings!&quot;&gt;</title></head>\n<body>\n<table>\n"
        );
    }

    #[test]
    fn test_end() {
        assert_eq!(end(true), "</table>\n</body>\n</html>\n");
    }

    #[test]
    fn test_row_1() {
        assert_eq!(
            row(&vec!["foo", "bar", "baz"], false, "", ""),
            "<tr><td>foo</td><td>bar</td><td>baz</td></tr>\n"
        )
    }

    #[test]
    fn test_row_2() {
        assert_eq!(
            row(&vec!["one", "two"], true, "x=1", "y=2"),
            "<tr x=1><th y=2>one</th><th y=2>two</th></tr>\n"
        )
    }
}
