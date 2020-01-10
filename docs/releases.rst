Releases
========

Version 3.0, Released January 10, 2020
--------------------------------------

* Drop support for Python 2 (it is end-of-life).
* Add support for subtests.
* Run a test suite with ``python -m tap``.
* Discontinue use of Pipenv for managing development.

Version 2.6.2, Released October 20, 2019
----------------------------------------

* Fix bug in streaming mode that would generate tap files
  when the plan was already set (affected pytest).

Version 2.6.1, Released September 17, 2019
------------------------------------------

* Fix TAP version 13 support from more-itertools behavior change.

Version 2.6, Released September 16, 2019
----------------------------------------

* Add support for Python 3.7.
* Drop support for Python 3.4 (it is end-of-life).

Version 2.5, Released September 15, 2018
----------------------------------------

* Add ``set_plan`` to ``Tracker`` which allows producing the ``1..N`` plan line
  before any tests.
* Switch code style to use Black formatting.


Version 2.4, Released May 29, 2018
----------------------------------

* Add support for producing TAP version 13 output
  to streaming and file reports
  by including the ``TAP version 13`` line.

Version 2.3, Released May 15, 2018
----------------------------------

* Add optional method to install tappy for YAML support
  with ``pip install tap.py[yaml]``.
* Make tappy version 13 compliant by adding support for parsing YAML blocks.
* ``unittest.expectedFailure`` now uses a TODO directive to better align
  with the specification.

Version 2.2, Released January 7, 2018
-------------------------------------

* Add support for Python 3.6.
* Drop support for Python 3.3 (it is end-of-life).
* Use Pipenv for managing development.
* Switch to pytest as the development test runner.

Version 2.1, Released September 23, 2016
----------------------------------------

* Add ``Parser.parse_text`` to parse TAP
  provided as a string.

Version 2.0, Released July 31, 2016
-----------------------------------

* Remove nose plugin.
  The plugin moved to the ``nose-tap`` distribution.
* Remove pytest plugin.
  The plugin moved to the ``pytest-tap`` distribution.
* Remove Pygments syntax highlighting plugin.
  The plugin was merged upstream directly into the Pygments project
  and is available without tappy.
* Drop support for Python 2.6.

Version 1.9, Released March 28, 2016
------------------------------------

* ``TAPTestRunner`` has a ``set_header`` method
  to enable or disable test case header ouput in the TAP stream.
* Add support for Python 3.5.
* Perform continuous integration testing on OS X.
* Drop support for Python 3.2.

Version 1.8, Released November 30, 2015
---------------------------------------

* The ``tappy`` TAP consumer can read a TAP stream
  directly from STDIN.
* Tracebacks are included as diagnostic output
  for failures and errors.
* The ``tappy`` TAP consumer has an alternative, shorter name
  of ``tap``.
* The pytest plugin now defaults to no output
  unless provided a flag.
  Users dependent on the old default behavior
  can use ``--tap-files`` to achieve the same results.
* Translated into Arabic.
* Translated into Chinese.
* Translated into Japanese.
* Translated into Russian.
* Perform continuous integration testing on Windows with AppVeyor.
* Improve unit test coverage to 100%.

Version 1.7, Released August 19, 2015
-------------------------------------

* Provide a plugin to integrate with pytest.
* Document some viable alternatives to tappy.
* Translated into German.
* Translated into Portuguese.

Version 1.6, Released June 18, 2015
-----------------------------------

* ``TAPTestRunner`` has a ``set_stream`` method to stream all TAP
  output directly to an output stream instead of a file.
  results in a single output file.
* The ``nosetests`` plugin has an optional ``--tap-stream`` flag to
  stream all TAP output directly to an output stream instead of a file.
* tappy is now internationalized. It is translated into Dutch, French,
  Italian, and Spanish.
* tappy is available as a Python wheel package, the new Python packaging
  standard.

Version 1.5, Released May 18, 2015
----------------------------------

* ``TAPTestRunner`` has a ``set_combined`` method to collect all
  results in a single output file.
* The ``nosetests`` plugin has an optional ``--tap-combined`` flag to
  collect all results in a single output file.
* ``TAPTestRunner`` has a ``set_format`` method to specify line format.
* The ``nosetests`` plugin has an optional ``--tap-format`` flag to specify
  line format.

Version 1.4, Released April 4, 2015
-----------------------------------

* Update ``setup.py`` to support Debian packaging. Include man page.

Version 1.3, Released January 9, 2015
-------------------------------------

* The ``tappy`` command line tool is available as a TAP consumer.
* The ``Parser`` and ``Loader`` are available as APIs for programmatic
  handling of TAP files and data.

Version 1.2, Released December 21, 2014
---------------------------------------

* Provide a syntax highlighter for Pygments so any project using Pygments
  (e.g., Sphinx) can highlight TAP output.

Version 1.1, Released October 23, 2014
--------------------------------------

* ``TAPTestRunner`` has a ``set_outdir`` method to specify where to store
  ``.tap`` files.
* The ``nosetests`` plugin has an optional ``--tap-outdir`` flag to specify
  where to store ``.tap`` files.
* tappy has backported support for Python 2.6.
* tappy has support for Python 3.2, 3.3, and 3.4.
* tappy has support for PyPy.

Version 1.0, Released March 16, 2014
------------------------------------

* Initial release of tappy
* ``TAPTestRunner`` - A test runner for ``unittest`` modules that generates
  TAP files.
* Provides a plugin for integrating with **nose**.
