tappy - TAP tools for Python
============================

tappy provides tools for working with the Test Anything Protocol (TAP) in
Python. tappy generates TAP output from your ``unittest`` test cases. You
can use the TAP output files with a tool like the `Jenkins TAP plugin
<https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin>`_ or any other TAP
consumer.

For the curious: tappy sounds like "happy."

Installation
------------

tappy is available for download from `PyPI
<https://pypi.python.org/pypi/tap.py>`_.  You can install it with Python's
standard install tools (e.g., ``pip``). tappy is currently supported on
Python 2.6, 2.7, 3.2, 3.3, 3.4, and PyPy.

.. code-block:: bash

   $ pip install tap.py

Documentation
-------------

.. toctree::
   :maxdepth: 2

   producers
   highlighter
   contributing
   releases
