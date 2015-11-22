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

    return get_status(result)


def parse_args(argv):
    description = _('A TAP consumer for Python')
    epilog = _(
        'When no files are given or a dash (-) is used for the file name, '
        'tappy will read a TAP stream from STDIN.')
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        'files', metavar='FILE', nargs='*', help=_(
            'A file containing TAP output. Any directories listed will be '
            'scanned for files to include as TAP files.'))
    parser.add_argument(
        '-v', '--verbose', action='store_const', default=1, const=2,
        help=_('use verbose messages'))

    # argparse expects the executable to be removed from argv.
    args = parser.parse_args(argv[1:])
    return args


def get_status(result):
    """Get a return status from the result."""
    if result.wasSuccessful():
        return 0
    else:
        return 1
