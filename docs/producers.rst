TAP Producers
=============

**tappy** integrates with ``unittest`` based test cases to generate TAP output.
The producers come in two varieties: support with only the standard library
and support for `nose <https://nose.readthedocs.org/en/latest/>`_.

* ``TAPTestRunner`` - This subclass of ``unittest.TextTestRunner`` provides all
  the functionality of ``TextTestRunner`` and generates TAP files.
* **tappy** for **nose** - **tappy** provides a plugin (simply called ``TAP``)
  for the **nose** testing tool.

Examples
--------

TODO: provide samples of both plugins in use.
