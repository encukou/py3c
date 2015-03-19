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

    If you want something to print out a stick on your wall,
    use this – compared to the other docs, you'll save trees.

* :doc:`Definition Summary <defs>`

    A **table** summarizing how py3c's macros are defined.
    Convenient if you already know the differences between Python 2 and 3,
    or before a dive into py3c's internals.

    Also serves as a summary of where py3c provides the
    Python 3 API, and where it resorts to inventing its own macros.

* :ref:`Index <genindex>` and :ref:`Search <search>`

    Head here if you're looking for something specific.


.. toctree::
   :hidden:

   guide
   cheatsheet
   defs
