#! /usr/bin/env python
# csv2html
# Copyright (c) 2013, 2014, 2017 dbohdan. All rights reserved.
# License: BSD-3. See the file LICENSE.

from csv2html import csv2html
import os.path
import unittest
import StringIO

TEST_PATH = os.path.dirname(os.path.realpath(__file__))


def read_file(filename):
    with open(os.path.join(TEST_PATH, filename), "rb") as f:
        content = f.read().decode("utf-8")
    return content


def convert_test_data(filename="test.csv", **kwargs):
    output = StringIO.StringIO()
    with open(os.path.join(TEST_PATH, "test.csv"), "rb") as input:
        csv2html.convert_csv_to_html(input, output, **kwargs)
    return output.getvalue().decode("utf-8")


class TestCsv2html(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_default(self):
        self.assertEqual(read_file("test-default.html"), convert_test_data())

    def test_completedoc_and_title(self):
        self.assertEqual(
            read_file("test-c-t.html"),
            convert_test_data(title="Foo & Bar", completedoc=True)
        )

    def test_renum(self):
        self.assertEqual(
            read_file("test-r.html"),
            convert_test_data(renum=True)
        )

    def test_nstart(self):
        self.assertEqual(
            read_file("test-s5.html"),
            convert_test_data(nstart=5)
        )

    def test_nstart_and_skipheader(self):
        self.assertEqual(
            read_file("test-s5-n.html"),
            convert_test_data(nstart=5, skipheader=True)
        )

if __name__ == '__main__':
    unittest.main()
