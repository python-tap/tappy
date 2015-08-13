# Copyright (c) 2015, Matt Layman

from tap.plugins import labels
from tap.tracker import Tracker

# Because of how pytest hooks work, there is not much choice
# except to use module level state. Ugh.
tracker = Tracker()


def pytest_addoption(parser):
    """Include all the command line options."""
    group = parser.getgroup('terminal reporting', after='general')
    group.addoption('--tap-outdir', metavar='path', help=labels.OUTDIR_HELP)


def pytest_configure(config):
    """Set all the options before the test run."""
    tracker.outdir = config.option.tap_outdir


def pytest_itemcollected(item):
    """Track the test result."""


def pytest_collectreport(report):
    """Dump the results."""
