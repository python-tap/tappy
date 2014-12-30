tappy - TAP tools for Python
============================

tappy provides tools for working with the Test Anything Protocol (TAP) in
Python.

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
Python 2.6, 2.7, 3.2, 3.3, 3.4, and PyPy.

.. code-block:: bash

   $ pip install tap.py

Documentation
-------------

.. toctree::
   :maxdepth: 2

   producers
   consumers
   highlighter
   contributing
   releases
