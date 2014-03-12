Design Goals
============

Motivation
----------

Some projects have extremely heterogenous programming environments with many
programming languages and tools. Because of the simplicity of TAP, the
protocol can function as a *lingua franca* for testing. When every testing
tool on a project can create TAP, a team can get a holistic view of
their system. Python does not have a bridge from ``unittest`` to TAP so it is
difficult to integrate a Python test suite into a larger TAP ecosystem.

TAP is simple so **tappy** is trying to remove the integration barrier.

Goals
-----

1. Provide `TAP Producers <http://testanything.org/producers.html>`_ which
   translate Python's ``unittest`` into TAP.
2. Provide a `TAP Consumer <http://testanything.org/consumers.html>`_ which
   reads TAP and provides a programmatic API in Python or generates summary
   results.
3. Provide a command line interface for reading TAP.

