# Copyright (c) 2015, Matt Layman

from tap.i18n import _
from tap.tracker import Tracker

# Because of how pytest hooks work, there is not much choice
# except to use module level state. Ugh.
tracker = Tracker()


def pytest_addoption(parser):
    """Include all the command line options."""
    group = parser.getgroup('terminal reporting', after='general')
    group.addoption('--tap-outdir', metavar='path', help=_(
        'An optional output directory to write TAP files to. '
        'If the directory does not exist, it will be created.'))
    # TODO: Add remaining options.
    # TODO: Figure out how to suppress pytext terminal output.


def pytest_configure(config):
    """Set all the options before the test run."""
    tracker.outdir = config.option.tap_outdir
    # TODO: Set options on tracker.


def pytest_itemcollected(item):
    """Track the test result."""
    # TODO: Put the result into the tracker with proper description.


def pytest_collectreport(report):
    """Dump the results."""
    # TODO: Dump out the results to files.
