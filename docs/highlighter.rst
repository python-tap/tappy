TAP Syntax Highlighter for Pygments
===================================

tappy implements a `Pygments <http://pygments.org/>`_ extension for syntax
highlighting of TAP files. Any project that uses Pygments, like
`Sphinx <http://sphinx-doc.org/>`_, can take advantage of this feature.
Below is an example usage for Sphinx.

.. code-block:: rst

   .. code-block:: tap

      1..2
      ok 1 - A passing test.
      not ok 2 - A failing test.
