Alternatives
============

tappy is not the only project that can produce TAP output for Python.
While tappy is a capable TAP producer and consumer,
other projects might be a better fit for you.
The following comparison lists some other Python TAP tools
and lists some of the biggest differences compared to tappy.

pycotap
-------

pycotap is a good tool for when you want TAP output,
but you don't want extra dependencies.
pycotap is a zero dependency TAP producer.
It is so small that you could even embed it into your project.
`Check out the project homepage
<https://el-tramo.be/pycotap/>`_.

catapult
--------

catapult is a TAP producer.
catapult is also capable of producing TAP-Y and TAP-J
which are YAML and JSON test streams
that are inspired by TAP.
`You can find the catapult source on GitHub
<https://github.com/jcelliott/catapult>`_.

pytap13
-------

pytap13 is a TAP consumer for TAP version 13.
It parses a TAP stream
and produces test instances that can be inspected.
`pytap13's homepage is on Bitbucket
<https://bitbucket.org/fedoraqa/pytap13>`_.

bayeux
------

bayeux is a TAP producer
that is designed to work with unittest and unittest2.
`bayeux is on GitLab.
<https://gitlab.com/mcepl/bayeux>`_.

taptaptap
---------

taptaptap is a TAP producer with a procedural style
similar to Perl.
It also includes a ``TapWriter`` class as a TAP producer.
`Visit the taptaptap homepage
<http://lukas-prokop.at/proj/taptaptap/>`_.

unittest-tap-reporting
----------------------

unittest-tap-reporting is another zero dependency TAP producer.
`Check it out on GitHub
<https://github.com/vit1251/unittest-tap-reporting>`_.

If there are other relevant projects,
please post an issue on GitHub
so this comparison page can be updated accordingly.
