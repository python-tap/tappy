tappy - TAP tools for Python
============================

.. image:: images/tap.png

tappy provides tools for working with the
`Test Anything Protocol (TAP) <http://testanything.org>`_
in Python.

tappy generates TAP output from your ``unittest`` test cases. You
can use the TAP output files with a tool like the `Jenkins TAP plugin
<https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin>`_ or any other TAP
consumer.

tappy also provides a ``tappy`` command line tool as a TAP consumer. This tool
can read TAP files and display the results like a normal Python test runner.
tappy provides other TAP consumers via Python APIs for programmatic access to
TAP files.

For the curious: tappy sounds like "happy."

Installation
------------

tappy is available for download from `PyPI
<https://pypi.python.org/pypi/tap.py>`_. tappy is currently supported on
Python
3.5,
3.6,
3.7,
and PyPy.
It is continuously tested on Linux, OS X, and Windows.

.. code-block:: console

   $ pip install tap.py

TAP version 13 brings support for YAML blocks
for `YAML blocks <http://testanything.org/tap-version-13-specification.html#yaml-blocks>`_
associated with test results.
To work with version 13, install the optional dependencies.
Learn more about YAML support in the :ref:`tap-version-13` section.

.. code-block:: console

   $ pip install tap.py[yaml]

Quickstart
----------

tappy can run like the built-in ``unittest`` discovery runner.

.. code-block:: console

   $ python -m tap

This should be enough to run a unittest-based test suite
and output TAP to the console.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   producers
   consumers
   highlighter
   contributing
   alternatives
   releases
