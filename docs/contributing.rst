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

tappy uses Pipenv
to manage development.
The following instructions assume that Pipenv is installed.
See the `Pipenv install instructions <https://docs.pipenv.org/install/>`_
for more details.

After installing Pipenv:

.. code-block:: console

   $ git clone git@github.com:python-tap/tappy.git
   $ cd tappy
   $ pipenv install --dev --ignore-pipfile
   $ pipenv shell
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
