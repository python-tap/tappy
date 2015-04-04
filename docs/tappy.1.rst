:orphan:

tappy manual page
=================

Synopsis
--------

**tappy** [*options*] <*pathname*> [*pathname* ...]


Description
-----------

The :program:`tappy` command consumes the list of tap files
given as *pathname* s and produces an output similar to what
the regular text test-runner from python's :py:mod:`unittest`
module would. If *pathname* points to a directory,
:program:`tappy` will look in that directory of ``*.tap``
files to consume.

If you have a tool that consumes the `unittest` regular output,
but wish to use the TAP protocol to better integrate with other
tools, you may use tappy to *replay* tests from .tap files,
without having to actually run the tests again (which is much
faster).

It is also an example of how to use the tap consumer API
provided by the :py:mod:`tap` module.

.. warning::

   :program:`tappy`'s output will differ from the standard
   :py:mod:`unittest` output. Indeed it cannot reproduce error
   and failure messages (e.g. stack traces, ...) that are not
   recorded in tap files.

Options
-------

-h, --help     show a short description and option list
               and exit.
-v, --verbose  produce verbose output


Aliases
-------

When installed from a Debian package, the tappy command can be
run against a specific python interpreter. Debian's current
policy with respect to Python is to favor Python 3. Thus, if
you install the :file:`python3-tappy` package, :program:`tappy`
will run with Python 3. You can use the
:manpage:`update-alternatives(1)` command to change that
behaviour and favor the version running against Python 2.

Alternatively you can select the interpreter, by explicitly
choosing either of the :program:`python-tappy` and
:program:`python3-tappy` commands.

:manpage:`tappy(1)`, :manpage:`python-tappy(1)`, :manpage:`python3-tappy(1)`


Author
------

The :program:`tappy` and the :py:mod:`tap` modules were written
by Matt LAYMAN (https://github.com/mblayman/tappy).

This manual page was written Nicolas CANIART, for the Debian project.

