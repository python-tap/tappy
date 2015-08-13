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


def pytest_configure(config):
    """Set all the options before the test run."""
    tracker.outdir = config.option.tap_outdir


def pytest_itemcollected(item):
    """Track the test result."""


def pytest_collectreport(report):
    """Dump the results."""
