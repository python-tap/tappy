Contributing
============

tappy should be easy to contribute to. If anything is unclear about how to
contribute, please submit an issue on GitHub so that we can fix it!

How
-----

Fork tappy on `GitHub <https://github.com/python-tap/tappy>`_ and
`submit a Pull Request <https://help.github.com/articles/creating-a-pull-request/>`_
when you're ready.

Setup
-----

tappy uses the built-in `venv` module.

.. code-block:: console

   $ git clone git@github.com:python-tap/tappy.git
   $ cd tappy
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install -r requirements-dev.txt
   $ # Edit some files and run the tests.
   $ pytest

The commands above show how to get a tappy clone configured.
If you've executed those commands
and the test suite passes,
you should be ready to develop.

Guidelines
----------

1. Code uses Black style. Please run it through ``black tap`` to autoformat.
2. Make sure your change works against master! (Bonus points for unit tests.)
3. Document your change in the ``docs/releases.rst`` file.
4. For first time contributors, please add your name to ``AUTHORS``
   so you get attribution for you effort.
   This is also to recognize your claim to the copyright in the project.
