TAP Producers
=============

**tappy** integrates with ``unittest`` based test cases to produce TAP output.
The producers come in two varieties: support with only the standard library
and support for `nose <https://nose.readthedocs.org/en/latest/>`_.

* ``TAPTestRunner`` - This subclass of ``unittest.TextTestRunner`` provides all
  the functionality of ``TextTestRunner`` and generates TAP files.
* **tappy** for **nose** - **tappy** provides a plugin (simply called ``TAP``)
  for the **nose** testing tool.

Both producers will create one TAP file for each ``TestCase`` executed by the
test suite. The files will use the name of the test case class with a ``.tap``
extension. For example:

.. code-block:: python

   class TestFoo(unittest.TestCase):

       def test_identity(self):
           '''Test numeric equality as an example.'''
           self.assertTrue(1 == 1)

The class will create a file named ``TestFoo.tap`` containing the following. ::

    # TAP results for TestFoo
    ok 1 - Test numeric equality as an example. 
    1..1

Examples
--------

The ``TAPTestRunner`` works like the ``TextTestRunner``. To use the runner,
load test cases using the ``TestLoader`` and pass the tests to the run method.
The sample below is the test runner used with **tappy**'s own tests.

.. literalinclude:: ../tap/tests/run.py
   :lines: 3-

Running **tappy** with **nose** is as straightforward as enabling the plugin
when calling ``nosetests``.

.. code-block:: sh

   $ nosetests --with-tap
   ...............
   ----------------------------------------------------------------------
   Ran 15 tests in 0.020s

   OK
