Contributing
============

tappy should be easy to contribute to. If anything is unclear about how to
contribute, please submit an issue on GitHub so that we can fix it!

How
---

Fork tappy on `GitHub <https://github.com/python-tap/tappy>`_ and
`submit a Pull Request <https://help.github.com/articles/creating-a-pull-request/>`_
when you're ready.

The goal of tappy is to be a TAP-compliant producer and consumer.
If you want to work on an issue
that is outside of the TAP spec,
please write up an issue first,
so we can discuss the change.

Setup
-----

tappy uses [uv](https://docs.astral.sh/uv/) for development.

.. code-block:: console

   $ git clone git@github.com:python-tap/tappy.git
   $ cd tappy
   $ # Edit some files and run the tests.
   $ make test

The commands above show how to get a tappy clone configured.
If you've executed those commands
and the test suite passes,
you should be ready to develop.

Guidelines
----------

1. Code uses Ruff for formatting and linting.
   If you have `pre-commit`, you can add ruff hooks via `pre-commit install`.
   These hooks will run as part of CI.
   Changes will not be accepted unless CI passes.
2. Make sure your change works with unit tests.
3. Document your change in the ``docs/releases.rst`` file.
4. For first time contributors, please add your name to ``AUTHORS``
   so you get attribution for you effort.
   This is also to recognize your claim to the copyright in the project.

Release checklist
-----------------

These are notes for my release process,
so I don't have to remember all the steps.
Other contributors are free to ignore this.

1. Update ``docs/releases.rst``.
2. Update version in ``pyproject.toml`` and ``tap/__init__.py``.
3. ``rm -rf dist && uv build``
4. ``uv publish``
5. ``git tag -a vX.X -m "Version X.X"``
6. ``git push --tags``
