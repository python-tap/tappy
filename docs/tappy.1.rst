:orphan:

tappy manual page
=================


Synopsis
--------

**tappy** [*options*] <*pathname*> [<*pathname*> ...]


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


Author
------

The :program:`tappy` and the :py:mod:`tap` modules were written
by Matt LAYMAN (https://github.com/mblayman/tappy).

This manual page was written Nicolas CANIART, for the Debian project.

