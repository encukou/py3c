..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Licensed under CC-BY-SA-3.0; see the license file


====================
Contributing to py3c
====================

.. highlight:: c

If you would like to contribute to py3c, be it code, documentation,
suggestions, or anything else, please file an issue or send a pull request
at the project's `Github page <http://github.com/encukou/py3c>`_.

If you are not familiar with Github, or prefer not to use it,
you can e-mail contributions to ``encukou`` at ``gmail`` dot ``com``.


Testing
=======

Automatic testing is set up at Travis CI:

    .. image:: https://travis-ci.org/encukou/py3c.svg?branch=master
       :alt: Build status

To test the code locally run (using GNU make)::

    $ make test

This will test py3c against ``python2`` and ``python3``. To test under a
different interpreter, run for example::

    $ make test-python35


