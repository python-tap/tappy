TAP Consumers
=============

tappy Tool
----------

The ``tappy`` command line tool is a `TAP consumer
<http://testanything.org/consumers.html>`_.
The tool accepts TAP files or directories containing TAP files
and provides a standard Python ``unittest`` style summary report.
Check out ``tappy -h`` for the complete list of options.
You can also use the tool's shorter alias of ``tap``.

.. code-block:: console

    $ tappy *.tap
    ................F..................................
    ======================================================================
    FAIL: <file=TestParser.tap>
    - The parser extracts a bail out line.
    ----------------------------------------------------------------------

    ----------------------------------------------------------------------
    Ran 51 tests in 0.002s

    FAILED (failures=1)

TAP Stream
~~~~~~~~~~

``tappy`` can read a TAP stream directly STDIN.
This permits any TAP producer to pipe its results to ``tappy``
without generating intermediate output files.
``tappy`` will read from STDIN
when no arguments are provided
or when a dash character is the only argument.

Here is an example of ``nosetests`` piping to ``tappy``:

.. code-block:: console

    $ nosetests --with-tap --tap-stream 2>&1 | tappy
    ......................................................................
    ...............................................
    ----------------------------------------------------------------------
    Ran 117 tests in 0.003s

    OK

In this example,
``nosetests`` puts the TAP stream on STDERR
so it must be redirected to STDOUT
because the Unix pipe expects input on STDOUT.

``tappy`` can use redirected input
from a shell.

.. code-block:: console

    $ tappy < TestAdapter.tap
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.000s

    OK

This final example shows ``tappy`` consuming TAP
from Perl's test tool, ``prove``.
The example includes the optional dash character.

.. code-block:: console

    $ prove t/array.t -v | tappy -
    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 0.001s

    OK

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

.. _tap-version-13:

TAP version 13
~~~~~~~~~~~~~~

The specification for TAP version 13 adds support for `yaml blocks <https://testanything.org/tap-version-13-specification.html#yaml-blocks>`_
to provide additional information about the preceding test. In order to consume
yaml blocks, ``tappy`` requires `pyyaml <https://pypi.org/project/PyYAML/>`_ and
`more-itertools <https://pypi.org/project/more-itertools/>`_ to be installed.

These dependencies are optional. If they are not installed, TAP output will still
be consumed, but any yaml blocks will be parsed as :class:`tap.line.Unknown`. If a
:class:`tap.line.Result` object has an associated yaml block, :attr:`~tap.line.Result.yaml_block`
will return the block converted to a ``dict``. Otherwise, it will return ``None``.

``tappy`` provides a strict interpretation of the specification. A yaml block will
only be associated with a result if it immediately follows that result. Any 
:class:`diagnostic <tap.line.Diagnostic>` between a :class:`result <tap.line.Result>` and a yaml
block will result in the block lines being parsed as :class:`tap.line.Unknown`.

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
