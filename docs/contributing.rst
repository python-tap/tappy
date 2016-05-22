Contributing
============

tappy should be easy to contribute to. If anything is unclear about how to
contribute, please submit an issue on GitHub so that we can fix it!

How
-----

Fork tappy on `GitHub <https://github.com/python-tap/tappy>`_ and submit a pull
request when you're ready.

Setup
-----

tappy uses a standard Python toolchain.
While many setups are possible,
the following should get you started quickly.
At minimum, you'll need 
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_
and
`pip <https://pip.pypa.io/en/stable/installing/>`_
to begin.

.. code-block:: console

   $ # Start from the root of a tappy clone.
   $ virtualenv venv                            # Create your virtual environment.
   $ source venv/bin/activate                   # Activate it.
   (venv)$ pip install -r requirements-dev.txt  # Install developer tools.
   (venv)$ pip install -e .                     # Install tappy in editable mode.
   (venv)$ nosetests                            # Run the test suite.

The commands above show how to get a tappy clone configured.
If you've executed those commands
and the test suite passes,
you should be ready to develop.

Guidelines
----------

1. Code should follow PEP 8 style. Please run it through ``pep8`` to check.
2. Please try to conform with any conventions seen in the code for consistency.
3. Make sure your change works against master! (Bonus points for unit tests.)
