TAP Syntax Highlighter for Pygments
===================================

`Pygments <http://pygments.org/>`_ contains an extension for syntax
highlighting of TAP files. Any project that uses Pygments, like
`Sphinx <http://sphinx-doc.org/>`_, can take advantage of this feature.

This highlighter was initially implemented in tappy.
Since the highlighter was merged into the upstream Pygments project,
tappy is no longer a requirement to get TAP syntax highlighting.

Below is an example usage for Sphinx.

.. code-block:: rst

   .. code-block:: tap

      1..2
      ok 1 - A passing test.
      not ok 2 - A failing test.
