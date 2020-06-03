#! /usr/bin/env python3
# Integration tests for csv2html.
# Copyright (c) 2013, 2014, 2017, 2020 D. Bohdan.
# License: BSD (3-clause).  See the file LICENSE.

import os.path
import sys
import unittest

from os import environ
from subprocess import run, PIPE


COMMAND = environ.get('CSV2HTML_COMMAND', 'csv2html')
TEST_PATH = os.path.dirname(os.path.realpath(__file__))


def data_file(filename):
    return os.path.join(TEST_PATH, filename)


def read_file(filename):
    with open(data_file(filename), 'rb') as f:
        content = f.read()
    return content


def run_csv2html(
    *args,
    filename='test.csv',
    stdin=None
):
    path = filename if filename == '-' else data_file(filename)

    return run(
        [COMMAND, path, *args],
        stdin=stdin,
        stderr=PIPE,
        stdout=PIPE,
    )


class TestCsv2html(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        # The sendmail exit codes are convenient for scripting, but they are
        # unavailable in Python on Windows.  We hard code them here instead.
        # The numbers come from POSIX sysexit.h.
        self.exitCodes = {
            'EX_OK': 0,
            'EX_DATAERR': 65,
            'EX_NOINPUT': 66,
            'EX_UNAVAILABLE': 69,
            'EX_SOFTWARE': 70,
            'EX_IOERR': 74
        }

    def test_default(self):
        self.assertEqual(
            run_csv2html().stdout,
            read_file('test-default.html'),
        )

    def test_stdin(self):
        with open(data_file('test.csv')) as f:
            self.assertEqual(
                run_csv2html(filename='-', stdin=f).stdout,
                read_file('test-default.html'),
            )

    def test_completedoc_and_title(self):
        self.assertEqual(
            run_csv2html(
                '--title', 'Foo & Bar',
                '--complete-document'
            ).stdout,
            read_file('test-c-t.html'),
        )

    def test_renum(self):
        self.assertEqual(
            run_csv2html('--renumber').stdout,
            read_file('test-r.html'),
        )

    def test_nstart(self):
        self.assertEqual(
            run_csv2html('--start', '5').stdout,
            read_file('test-s5.html'),
        )

    def test_nstart_and_skipheader(self):
        self.assertEqual(
            run_csv2html('--start', '5', '--no-header').stdout,
            read_file('test-s5-n.html'),
        )

    def test_attrs(self):
        self.assertEqual(
            run_csv2html(
                '--table', 'class="foo" id="bar"',
                '--tr', 'class="row"',
                '--th', 'class="hcell"',
                '--td', 'class="cell"',
            ).stdout,
            read_file('test-attrs.html'),
        )

    def test_no_file(self):
        completed = run_csv2html(filename='does-not-exist.csv')

        self.assertRegex(
            completed.stderr.decode('utf-8'),
            r'.*No such file or directory.*',
        )
        self.assertEqual(completed.returncode, self.exitCodes['EX_IOERR'])

    def test_garbage_file(self):
        completed = run_csv2html(filename='garbage')

        self.assertRegex(
            completed.stderr.decode('utf-8'),
            r'.*Can not parse.*',
        )
        self.assertEqual(completed.returncode, self.exitCodes['EX_DATAERR'])


if __name__ == '__main__':
    unittest.main()
