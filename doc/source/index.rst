py3c: Python 2/3 compatibility layer for C extensions
=====================================================

This is *py3c*, a library for easing porting C extensions to Python 3,
providing macros for *single-source compatibility* between
Python 2.6, 2.7, and 3.3+.
It could be described as "the `six <https://pypi.python.org/pypi/six>`_
for C extensions".

Pick the docs you wish to read:


* :doc:`Porting guide <guide>`

    A detailed **walkthrough** for porting to Python 3.
    Read if you wish to start porting a C extension to Python 3.

* :doc:`Cheatsheet <cheatsheet>`

    A **quick reference**, helpful if you're in the middle of porting.
    Also useful if you find yourself working on a project that someone else
    is porting, and don't understand what's going on.

* :doc:`Definition summary <defs>`

    A **table** summarizing how py3c's macros are defined.
    Convenient if you already know the differences between Python 2 and 3,
    or before a dive into py3c's internals.



Indices:

* :ref:`genindex`
* :ref:`search`



.. toctree::
   :hidden:

   guide
   cheatsheet
   defs
