# Copyright (c) 2016, Matt Layman

import argparse
import os

try:
    from unittest import mock
except ImportError:
    import mock

from tap.loader import Loader
from tap.main import build_suite, get_status, main, parse_args
from tap.tests import TestCase


class TestMain(TestCase):
    """Tests for tap.main"""

    def test_exits_with_error(self):
        """The main function returns an error status if there were failures."""
        argv = ['/bin/fake', 'fake.tap']
        stream = open(os.devnull, 'w')

        status = main(argv, stream=stream)

        self.assertEqual(1, status)

    def test_get_successful_status(self):
        result = mock.Mock()
        result.wasSuccessful.return_value = True
        self.assertEqual(0, get_status(result))

    @mock.patch.object(Loader, 'load_suite_from_stdin')
    def test_build_suite_from_stdin(self, load_suite_from_stdin):
        args = mock.Mock()
        args.files = []
        expected_suite = mock.Mock()
        load_suite_from_stdin.return_value = expected_suite
        suite = build_suite(args)
        self.assertEqual(expected_suite, suite)

    @mock.patch.object(Loader, 'load_suite_from_stdin')
    def test_build_suite_from_stdin_dash(self, load_suite_from_stdin):
        argv = ['/bin/fake', '-']
        args = parse_args(argv)
        expected_suite = mock.Mock()
        load_suite_from_stdin.return_value = expected_suite
        suite = build_suite(args)
        self.assertEqual(expected_suite, suite)

    @mock.patch('tap.main.sys.stdin')
    @mock.patch('tap.main.sys.exit')
    @mock.patch.object(argparse.ArgumentParser, 'print_help')
    def test_when_no_pipe_to_stdin(self, print_help, sys_exit, mock_stdin):
        argv = ['/bin/fake']
        mock_stdin.isatty = mock.Mock(return_value=True)
        parse_args(argv)
        self.assertTrue(print_help.called)
        self.assertTrue(sys_exit.called)
