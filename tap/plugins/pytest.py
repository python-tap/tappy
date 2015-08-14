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
    # TODO: Figure out how to suppress pytest terminal output.


def pytest_configure(config):
    """Set all the options before the test run."""
    tracker.outdir = config.option.tap_outdir
    # TODO: Set options on tracker.


def pytest_runtest_logreport(report):
    """Add a test result to the tracker."""
    if report.when != 'call':
        return
    description = report.location[2]
    testcase = description.split('.', 1)[0]
    if report.outcome == 'passed':
        tracker.add_ok(testcase, description)
    elif report.outcome == 'failed':
        tracker.add_not_ok(testcase, description)
    elif report.outcome == 'skipped':
        reason = report.longrepr[2].split(':', 1)[1].strip()
        tracker.add_skip(testcase, description, reason)


def pytest_unconfigure(config):
    """Dump the results."""
    tracker.generate_tap_reports()
