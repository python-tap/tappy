TAP Producers
=============

tappy integrates with ``unittest`` based test cases to produce TAP output.
The producers come in two varieties: support with only the standard library
and support for `nose <https://nose.readthedocs.org/en/latest/>`_.

* ``TAPTestRunner`` - This subclass of ``unittest.TextTestRunner`` provides all
  the functionality of ``TextTestRunner`` and generates TAP files.
* tappy for **nose** - tappy provides a plugin (simply called ``TAP``)
  for the **nose** testing tool.

Both producers will create one TAP file for each ``TestCase`` executed by the
test suite. The files will use the name of the test case class with a ``.tap``
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

TAPTestRunner
-------------

The ``TAPTestRunner`` gives the user the ability to set the output directory.
Use the ``set_outdir`` class method.

.. code-block:: python

    # Either set it from the class or from a runner instance.
    TAPTestRunner.set_outdir('/my/output/directory')
    runner = TAPTestRunner()
    runner.set_outdir('/my/output/directory')

nose TAP Plugin
---------------

The **nose** TAP plugin also supports an optional output directory when you
don't want to store the ``.tap`` files wherever you executed ``nosetests``. Use
``--tap-outdir`` followed by a directory path to store the files in a different
place. The directory will be created if it does not exist.

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
