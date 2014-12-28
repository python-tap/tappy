# Copyright (c) 2014, Matt Layman

import argparse
import sys
import unittest

from tap.adapter import Adapter


def main(argv=sys.argv):
    """Entry point for ``tappy`` command."""
    args = parse_args(argv)

    # TODO: Factor out into a loader.
    # TODO: Handle directories.
    suite = unittest.TestSuite()
    for filename in args.files:
        suite.addTest(Adapter(filename))

    runner = unittest.TextTestRunner(verbosity=args.verbose)
    runner.run(suite)


def parse_args(argv):
    description = 'A TAP consumer for Python'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'files', metavar='FILE', nargs='+', help=(
            'A file containing TAP output. Any directories listed will be '
            'scanned for files to include as TAP files.'))
    parser.add_argument(
        '-v', '--verbose', action='store_const', default=1, const=2,
        help='use verbose messages')

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])
    return args
