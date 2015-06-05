tappy
=====

[![PyPI version][pypishield]](https://pypi.python.org/pypi/tap.py)
[![BSD license][license]](https://raw.githubusercontent.com/mblayman/tappy/master/LICENSE)
[![Downloads][shield]](https://pypi.python.org/pypi/tap.py)
[![Build Status][travis]](https://travis-ci.org/mblayman/tappy)

<img align="right" src="https://github.com/mblayman/tappy/blob/master/tap.png" 
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
on Python 2.6, 2.7, 3.2, 3.3, 3.4 and PyPy.
tappy is also translated into Dutch, French, Italian, and Spanish.

```bash
$ pip install tap.py
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
*   tappy for [nose][ns] - tappy provides a plugin for the **nose**
    testing tool.

Consumers
---------

*   `tappy` - A command line tool for processing TAP files.
*   `Loader` and `Parser` - Python APIs for handling of TAP files and data.

[tap]: http://testanything.org/
[pypishield]: https://img.shields.io/pypi/v/tap.py.svg
[license]: https://img.shields.io/pypi/l/tap.py.svg
[shield]: https://img.shields.io/pypi/dm/tap.py.svg
[travis]: https://travis-ci.org/mblayman/tappy.png?branch=master
[rtd]: http://tappy.readthedocs.org/en/latest/
[pypi]: https://pypi.python.org/pypi/tap.py
[stream]: https://github.com/mblayman/tappy/blob/master/stream.gif
[produce]: http://testanything.org/producers.html
[consume]: http://testanything.org/consumers.html
[ns]: https://nose.readthedocs.org/en/latest/
