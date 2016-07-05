
============
py3c Changes
============


Version History
===============

v0.7 (2016-07-05)
-----------------

Packaging:

* Fix file shim tests on big endian architectures (bug in testsuite only)


v0.6 (2016-05-19)
-----------------

Packaging:

* Fix file permissions when doing ``make instal``


v0.5 (2016-05-13)
-----------------

Packaging:

* Fix the pkgconfig file


v0.4 (2016-05-13)
-----------------

Fixes:

* Fix unterminated #if in tpflags.h (thanks to MURAOKA Yusuke)

Additions:

* Support for C++ (with initial help from MURAOKA Yusuke)
* Support PyFloat_FromString (thanks to Christoph Zwerschke)
* Test suite is much more comprehensive


v0.3 (2015-09-09)
-----------------

Breaking changes:

* Type flags moved to "tpflags.h", which is not included by default.
  See the warning in the file, or in documentation.

Other changes:

* Integrated capsulethunk.h
* Added PyFile_AsFile shim
* Discuss porting type definitions in the guide


v0.2 (2015-08-25)
-----------------

* First tagged public release


More Details
============

For all changes, see the `commit history on Github <https://github.com/encukou/py3c/commits/master>`_.
