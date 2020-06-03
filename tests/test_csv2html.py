#! /usr/bin/env python3
# Integration tests for csv2html.
# Copyright (c) 2013, 2014, 2017, 2020 D. Bohdan.
# License: BSD (3-clause).  See the file LICENSE.

import os.path
import sys
import unittest

from io import StringIO
from subprocess import run


TEST_PATH = os.path.dirname(os.path.realpath(__file__))


def read_file(filename):
    with open(os.path.join(TEST_PATH, filename), 'rb') as f:
        content = f.read()
    return content


def convert_test_data(*args, command='csv2html', filename='test.csv'):
    return run(
        [command, os.path.join(TEST_PATH, filename), *args],
        capture_output=True
    ).stdout


class TestCsv2html(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_default(self):
        self.assertEqual(
            read_file('test-default.html'),
            convert_test_data()
        )

    def test_completedoc_and_title(self):
        self.assertEqual(
            read_file('test-c-t.html'),
            convert_test_data('--title', 'Foo & Bar', '--complete-document')
        )

    def test_renum(self):
        self.assertEqual(
            read_file('test-r.html'),
            convert_test_data('--renumber')
        )

    def test_nstart(self):
        self.assertEqual(
            read_file('test-s5.html'),
            convert_test_data('--start', '5')
        )

    def test_nstart_and_skipheader(self):
        self.assertEqual(
            read_file('test-s5-n.html'),
            convert_test_data('--start', '5', '--no-header')
        )

    def test_attrs(self):
        self.assertEqual(
            read_file('test-attrs.html'),
            convert_test_data(
                '--table', 'class="foo" id="bar"',
                '--tr', 'class="row"',
                '--th', 'class="hcell"',
                '--td', 'class="cell"',
            )
        )


if __name__ == '__main__':
    unittest.main()
