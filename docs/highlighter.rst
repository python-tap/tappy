TAP Syntax Highlighter for Pygments
===================================

tappy implements a Pygments extension for syntax highlighting of TAP files. Any
project that uses Pygments, like Sphinx, can take advantage of this feature.
Below is an example usage for Sphinx.

.. code-block:: rst

   .. code-block:: tap

      1..2
      ok 1 - A passing test.
      not ok 2 - A failing test.
