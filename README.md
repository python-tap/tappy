tappy
=====

Tools for working with the Test Anything Protocol (TAP) in Python

Full documentation for **tappy** is at [Read the Docs][rtd]. The information
below provides a synopsis of what **tappy** supplies.

For the curious: **tappy** sounds like "happy."

Motivation
----------

Some projects have extremely heterogenous programming environments with many
programming languages and tools. Because of the simplicity of TAP, the
protocol can function as a *lingua franca* for testing. When every testing
tool on a project can create TAP, a team can get a holistic view of
their system. Python does not have a bridge from `unittest` to TAP so it is
difficult to integrate a Python test suite into a larger TAP ecosystem.

TAP is simple so **tappy** is trying to remove the integration barrier.

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
*   **tappy** for [nose][ns] - **tappy** provides a plugin for the **nose**
    testing tool.

TODOs
-----

This project is very young. There is lots to do.

*   TODO: Have options for either 1 big TAP file or 1 file per test case.
*   TODO: Create an API similar to Test::Harness (if it makes sense to do so) to provide programmatic access to TAP results within Python programs.
*   TODO: Create an executable `tappy` which should function like `prove`.
*   TODO: Use travis to do an end to end test. Run the test suite to generate
    TAP and use `tappy` to parse and verify the results. The results should
    always be the same.
*   TODO: Use travis to run the test runner and nosetests. Both paths need to
    always work.
*   TODO: provide Sphinx documentation at read the docs.

[rtd]: http://tappy.readthedocs.org/en/latest/
[produce]: http://testanything.org/producers.html
[consume]: http://testanything.org/consumers.html
[ns]: https://nose.readthedocs.org/en/latest/
