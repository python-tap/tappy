# Copyright (c) 2015, Matt Layman

import argparse
import sys
import unittest

from tap.i18n import _
from tap.loader import Loader


def main(argv=sys.argv, stream=sys.stderr):
    """Entry point for ``tappy`` command."""
    args = parse_args(argv)

    loader = Loader()
    suite = loader.load(args.files)

    runner = unittest.TextTestRunner(verbosity=args.verbose, stream=stream)
    result = runner.run(suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1


def parse_args(argv):
    description = _('A TAP consumer for Python')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'files', metavar='FILE', nargs='+', help=_(
            'A file containing TAP output. Any directories listed will be '
            'scanned for files to include as TAP files.'))
    parser.add_argument(
        '-v', '--verbose', action='store_const', default=1, const=2,
        help=_('use verbose messages'))

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])
    return args
