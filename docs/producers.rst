TAP Producers
=============

tappy integrates with ``unittest`` based test cases to produce TAP output.
The producers come in two varieties: support with only the standard library
and support for `nose <https://nose.readthedocs.org/en/latest/>`_.

* ``TAPTestRunner`` - This subclass of ``unittest.TextTestRunner`` provides all
  the functionality of ``TextTestRunner`` and generates TAP files or streams.
* tappy for **nose** - tappy provides a plugin (simply called ``TAP``)
  for the **nose** testing tool.

By default, both producers will create one TAP file for each ``TestCase``
executed by the test suite.
The files will use the name of the test case class with a ``.tap``
extension. For example:

.. code-block:: python

   class TestFoo(unittest.TestCase):

       def test_identity(self):
           """Test numeric equality as an example."""
           self.assertTrue(1 == 1)

The class will create a file named ``TestFoo.tap`` containing the following.

.. code-block:: tap

    # TAP results for TestFoo
    ok 1 - Test numeric equality as an example.
    1..1

The producers also have streaming modes which bypass the default runner
output and write TAP to the output stream instead of files. This is useful
for piping output directly to tools that read TAP natively.

.. code-block:: tap

    $ nosetests --with-tap --tap-stream tap.tests.test_parser
    # TAP results for TestParser
    ok 1 - test_after_hash_is_not_description (tap.tests.test_parser.TestParser)
    ok 2 - The parser extracts a bail out line.
    ok 3 - The parser extracts a diagnostic line.
    ok 4 - The TAP spec dictates that anything less than 13 is an error.
    ok 5 - test_finds_description (tap.tests.test_parser.TestParser)
    ok 6 - The parser extracts a not ok line.
    ok 7 - The parser extracts a test number.
    ok 8 - The parser extracts an ok line.
    ok 9 - The parser extracts a plan line.
    ok 10 - The parser extracts a plan line containing a SKIP.
    1..10

Examples
--------

The ``TAPTestRunner`` works like the ``TextTestRunner``. To use the runner,
load test cases using the ``TestLoader`` and pass the tests to the run method.
The sample below is the test runner used with tappy's own tests.

.. literalinclude:: ../tap/tests/run.py
   :lines: 3-

Running tappy with **nose** is as straightforward as enabling the plugin
when calling ``nosetests``.

.. code-block:: sh

   $ nosetests --with-tap
   ...............
   ----------------------------------------------------------------------
   Ran 15 tests in 0.020s

   OK

The configuration options for each TAP tool are listed
in the following sections.

TAPTestRunner
-------------

You can configure the ``TAPTestRunner`` from a set of class or instance
methods.

* ``set_stream`` - Enable streaming mode to send TAP output directly to
  the output stream. Use the ``set_stream`` instance method.

  .. code-block:: python

      runner = TAPTestRunner()
      runner.set_stream(True)

* ``set_outdir`` - The ``TAPTestRunner`` gives the user the ability to
  set the output directory. Use the ``set_outdir`` class method.

  .. code-block:: python

      TAPTestRunner.set_outdir('/my/output/directory')

* ``set_combined`` - TAP results can be directed into a single output file.
  Use the ``set_combined`` class method to store the results in
  ``testresults.tap``.

  .. code-block:: python

      TAPTestRunner.set_combined(True)

* ``set_format`` - Use the ``set_format`` class method to change the
  format of result lines.  ``{method_name}`` and ``{short_description}``
  are available options.

  .. code-block:: python

      TAPTestRunner.set_format('{method_name}: {short_description}')

nose TAP Plugin
---------------

The **nose** TAP plugin is configured from command line flags.

* ``--with-tap`` - This flag is required to enable the plugin.

* ``--tap-stream`` - Enable streaming mode to send TAP output directly to
  the output stream.

* ``--tap-outdir`` - The **nose** TAP plugin also supports an optional
  output directory when you don't want to store the ``.tap`` files
  wherever you executed ``nosetests``.

  Use ``--tap-outdir`` followed by a directory path to store the files
  in a different place. The directory will be created if it does not exist.

* ``--tap-combined`` - Store test results in a single output file
  in ``testresults.tap``.

* ``--tap-format`` - Provide a different format for the result lines.
  ``{method_name}`` and ``{short_description}`` are available options.
  For example, ``'{method_name}: {short_description}'``.
