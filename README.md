tappy
=====

[![PyPI version][fury]](https://pypi.python.org/pypi/tap.py)
[![Downloads][pypip]](https://pypi.python.org/pypi/tap.py)
[![Build Status][travis]](https://travis-ci.org/mblayman/tappy)

Tools for working with the Test Anything Protocol (TAP) in Python

Full documentation for tappy is at [Read the Docs][rtd]. The information
below provides a synopsis of what tappy supplies.

For the curious: tappy sounds like "happy."

Installation
------------

tappy is available for download from [PyPI][pypi]. You can install it with
`pip` or `easy_install`. tappy is currently supported on Python 2.6,
2.7, 3.2, 3.3, 3.4 and PyPy.

```bash
$ pip install tap.py
```

Motivation
----------

Some projects have extremely heterogenous programming environments with many
programming languages and tools. Because of the simplicity of TAP, the
protocol can function as a *lingua franca* for testing. When every testing
tool on a project can create TAP, a team can get a holistic view of
their system. Python did not have a bridge from `unittest` to TAP so it was
difficult to integrate a Python test suite into a larger TAP ecosystem.

tappy is Python's bridge to TAP.

Goals
-----

1.  Provide [TAP Producers][produce] which translate Python's `unittest` into
    TAP.
2.  Provide a [TAP Consumer][consume] which reads TAP and provides a
    programmatic API in Python or generates summary results.
3.  Provide a command line interface for reading TAP.

Producers
---------

*   `TAPTestRunner` - This subclass of `unittest.TextTestRunner` provides all
    the functionality of `TextTestRunner` and generates TAP files.
*   tappy for [nose][ns] - tappy provides a plugin for the **nose**
    testing tool.

TODOs
-----

There is a lot to do.

*   TODO: Have options for either 1 big TAP file or 1 file per test case.
*   TODO: Create an API similar to Test::Harness (if it makes sense to do so) to provide programmatic access to TAP results within Python programs.
*   TODO: Create an executable `tappy` which should function like `prove`.
*   TODO: Use travis to do an end to end test. Run the test suite to generate
    TAP and use `tappy` to parse and verify the results. The results should
    always be the same.

[fury]: https://badge.fury.io/py/tap.py.png
[pypip]: https://pypip.in/d/tap.py/badge.png
[travis]: https://travis-ci.org/mblayman/tappy.png?branch=master
[rtd]: http://tappy.readthedocs.org/en/latest/
[pypi]: https://pypi.python.org/pypi/tap.py
[produce]: http://testanything.org/producers.html
[consume]: http://testanything.org/consumers.html
[ns]: https://nose.readthedocs.org/en/latest/
