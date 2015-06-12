TAP Consumers
=============

tappy Tool
----------

The ``tappy`` command line tool is a `TAP consumer
<http://testanything.org/consumers.html>`_.
The tool accepts TAP files or directories containing TAP files
and provides a standard Python ``unittest`` style summary report.
Check out ``tappy -h`` for the complete list of options.

.. code-block:: bash

    $ tappy *.tap
    ................F..................................
    ======================================================================
    FAIL: <file=TestParser.tap>
    - The parser extracts a bail out line.
    ----------------------------------------------------------------------

    ----------------------------------------------------------------------
    Ran 51 tests in 0.002s

    FAILED (failures=1)

API
---

In addition to a command line interface, tappy enables programmatic access to
TAP files for users to create their own TAP consumers. This access comes in
two forms:

1. A ``Loader`` class which provides a ``load`` method to load a set of TAP
   files into a ``unittest.TestSuite``. The ``Loader`` can receive files or
   directories.

   .. code-block:: pycon

       >>> loader = Loader()
       >>> suite = loader.load(['foo.tap', 'bar.tap', 'baz.tap'])

2. A ``Parser`` class to provide a lower level interface. The ``Parser`` can
   parse a file via ``parse_file`` and return parsed lines that categorize the
   file contents.

   .. code-block:: pycon

       >>> parser = Parser()
       >>> for line in parser.parse_file('foo.tap'):
       ...     # Do whatever you want with the processed line.
       ...     pass

The API specifics are listed below.

.. autoclass:: tap.loader.Loader
   :members:

.. autoclass:: tap.parser.Parser
   :members:

Line Categories
~~~~~~~~~~~~~~~

The parser returns ``Line`` instances. Each line contains different properties
depending on its category.

.. autoclass:: tap.line.Result
   :members:

.. autoclass:: tap.line.Plan
   :members:

.. autoclass:: tap.line.Diagnostic
   :members:

.. autoclass:: tap.line.Bail
   :members:

.. autoclass:: tap.line.Version
   :members:

.. autoclass:: tap.line.Unknown
   :members:
