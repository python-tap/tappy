tappy
=====

[![PyPI version][pypishield]](https://pypi.python.org/pypi/tap.py)
[![Coverage][coverage]](https://codecov.io/github/python-tap/tappy)

<img align="right" src="https://github.com/python-tap/tappy/blob/main/docs/images/tap.png"
  alt="TAP logo" />

tappy is a set of tools for working with the
[Test Anything Protocol (TAP)][tap] in Python. TAP is a line based test
protocol for recording test data in a standard way.

Full documentation for tappy is at [Read the Docs][rtd]. The information
below provides a synopsis of what tappy supplies.

For the curious: tappy sounds like "happy."

If you find tappy useful, please consider starring the repository to show a
kindness and help others discover something valuable. Thanks!

Installation
------------

tappy is available for download from [PyPI][pypi]. tappy is currently supported
on Python
3.6,
3.7,
3.8,
3.9,
3.10,
and PyPy.
It is continuously tested on Linux, OS X, and Windows.

```bash
$ pip install tap.py
```

For testing with [pytest][pytest],
you only need to install `pytest-tap`.

```bash
$ pip install pytest-tap
```

For testing with [nose][ns],
you only need to install `nose-tap`.

```bash
$ pip install nose-tap
```

TAP version 13 brings support
for [YAML blocks](http://testanything.org/tap-version-13-specification.html#yaml-blocks)
associated with test results.
To work with version 13, install the optional dependencies.
Learn more about YAML support
in the [TAP version 13](http://tappy.readthedocs.io/en/latest/consumers.html#tap-version-13) section.

```bash
$ pip install tap.py[yaml]
```

Motivation
----------

Some projects have mixed programming environments with many
programming languages and tools. Because of TAP's simplicity,
it can function as a *lingua franca* for testing.
When every testing tool can create TAP,
a team can get a holistic view of their system.
Python did not have a bridge from `unittest` to TAP so it was
difficult to integrate a Python test suite into a larger TAP ecosystem.

tappy is Python's bridge to TAP.

![TAP streaming demo][stream]

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
*   tappy for [nose][ns] -
    `nose-tap` provides a plugin
    for the **nose** testing tool.
*   tappy for [pytest][pytest] -
    `pytest-tap` provides a plugin
    for the **pytest** testing tool.

Consumers
---------

*   `tappy` - A command line tool for processing TAP files.
*   `Loader` and `Parser` - Python APIs for handling of TAP files and data.

Contributing
------------

The project welcomes contributions of all kinds.
Check out the [contributing guidelines][contributing]
for tips on how to get started.

[tap]: http://testanything.org/
[pypishield]: https://img.shields.io/pypi/v/tap.py.svg
[coverage]: https://img.shields.io/codecov/c/github/python-tap/tappy.svg
[rtd]: http://tappy.readthedocs.io/en/latest/
[pypi]: https://pypi.python.org/pypi/tap.py
[stream]: https://github.com/python-tap/tappy/blob/main/docs/images/stream.gif
[produce]: http://testanything.org/producers.html
[consume]: http://testanything.org/consumers.html
[ns]: https://nose.readthedocs.io/en/latest/
[pytest]: http://pytest.org/latest/
[contributing]: http://tappy.readthedocs.io/en/latest/contributing.html
