==============
py3c reference
==============

.. highlight:: c

Compatibility layer
===================

::

    #include <py3c/compat.h>  // (included in <py3c.h>)


.. index:: PyStr

PyStr
~~~~~

.. c:var:: PyStr_Type

    | Python 2: :c:data:`PyString_Type <py2:PyString_Type>`
    | Python 3: :c:data:`PyUnicode_Type <py3:PyUnicode_Type>`

.. c:function:: PyStr_Check

    | Python 2: :c:func:`PyString_Check <py2:PyString_Check>`
    | Python 3: :c:func:`PyUnicode_Check <py3:PyUnicode_Check>`

.. c:function:: PyStr_CheckExact

    | Python 2: :c:func:`PyString_CheckExact <py2:PyString_CheckExact>`
    | Python 3: :c:func:`PyUnicode_CheckExact <py3:PyUnicode_CheckExact>`

.. c:function:: PyStr_FromString

    | Python 2: :c:func:`PyString_FromString <py2:PyString_FromString>`
    | Python 3: :c:func:`PyUnicode_FromString <py3:PyUnicode_FromString>`

.. c:function:: PyStr_FromStringAndSize

    | Python 2: :c:func:`PyString_FromStringAndSize <py2:PyString_FromStringAndSize>`
    | Python 3: :c:func:`PyUnicode_FromStringAndSize <py3:PyUnicode_FromStringAndSize>`

.. c:function:: PyStr_FromFormat

    | Python 2: :c:func:`PyString_FromFormat <py2:PyString_FromFormat>`
    | Python 3: :c:func:`PyUnicode_FromFormat <py3:PyUnicode_FromFormat>`

.. c:function:: PyStr_FromFormatV

    | Python 2: :c:func:`PyString_FromFormatV <py2:PyString_FromFormatV>`
    | Python 3: :c:func:`PyUnicode_FromFormatV <py3:PyUnicode_FromFormatV>`

.. c:function:: PyStr_AsString

    | Python 2: :c:func:`PyString_AsString <py2:PyString_AsString>`
    | Python 3: :c:func:`PyUnicode_AsUTF8 <py3:PyUnicode_AsUTF8>` (!)

.. c:function:: PyStr_Concat

    | Python 2: :c:func:`PyString_Concat <py2:PyString_Concat>`
    | Python 3: :c:func:`PyUnicode_Concat <py3:PyUnicode_Concat>`

.. c:function:: PyStr_Format

    | Python 2: :c:func:`PyString_Format <py2:PyString_Format>`
    | Python 3: :c:func:`PyUnicode_Format <py3:PyUnicode_Format>`

.. c:function:: PyStr_InternInPlace

    | Python 2: :c:func:`PyString_InternInPlace <py2:PyString_InternInPlace>`
    | Python 3: :c:func:`PyUnicode_InternInPlace <py3:PyUnicode_InternInPlace>`

.. c:function:: PyStr_InternFromString

    | Python 2: :c:func:`PyString_InternFromString <py2:PyString_InternFromString>`
    | Python 3: :c:func:`PyUnicode_InternFromString <py3:PyUnicode_InternFromString>`

.. c:function:: PyStr_Decode

    | Python 2: :c:func:`PyString_Decode <py2:PyString_Decode>`
    | Python 3: :c:func:`PyUnicode_Decode <py3:PyUnicode_Decode>`

.. c:function:: PyStr_AsUTF8String(str)

    | Python 2: :c:func:`PyString_AsEncodedObject(str, "UTF-8", "strict") <py2:PyString_AsEncodedObject>`
    | Python 3: :c:func:`PyUnicode_AsUTF8String(str) <py3:PyUnicode_AsUTF8String>`

.. c:function:: PyStr_AsUTF8AndSize(str, sizeptr)

    | Python 2: (\*sizeptr = :c:func:`PyString_Size(str) <py2:PyString_Size>`, :c:func:`PyString_AsString(str) <py2:PyString_AsString>`)
    | Python 3: :c:func:`PyUnicode_AsUTF8AndSize(str, sizeptr) <py3:PyUnicode_AsUTF8AndSize>`


.. index:: PyBytes

PyBytes
~~~~~~~

.. c:var:: PyBytes_Type

    | Python 2: :c:data:`PyString_Type <py2:PyString_Type>`
    | Python 3: :c:data:`(provided) <py3:PyBytes_Type>`

.. c:function:: PyBytes_Check

    | Python 2: :c:func:`PyString_Check <py2:PyString_Check>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_Check>`

.. c:function:: PyBytes_CheckExact

    | Python 2: :c:func:`PyString_CheckExact <py2:PyString_CheckExact>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_CheckExact>`

.. c:function:: PyBytes_FromString

    | Python 2: :c:func:`PyString_FromString <py2:PyString_FromString>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_FromString>`

.. c:function:: PyBytes_FromStringAndSize

    | Python 2: :c:func:`PyString_FromStringAndSize <py2:PyString_FromStringAndSize>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_FromStringAndSize>`

.. c:function:: PyBytes_FromFormat

    | Python 2: :c:func:`PyString_FromFormat <py2:PyString_FromFormat>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_FromFormat>`

.. c:function:: PyBytes_FromFormatV

    | Python 2: :c:func:`PyString_FromFormatV <py2:PyString_FromFormatV>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_FromFormatV>`

.. c:function:: PyBytes_Size

    | Python 2: :c:func:`PyString_Size <py2:PyString_Size>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_Size>`

.. c:function:: PyBytes_GET_SIZE

    | Python 2: :c:func:`PyString_GET_SIZE <py2:PyString_GET_SIZE>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_GET_SIZE>`

.. c:function:: PyBytes_AsString

    | Python 2: :c:func:`PyString_AsString <py2:PyString_AsString>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_AsString>`

.. c:function:: PyBytes_AS_STRING

    | Python 2: :c:func:`PyString_AS_STRING <py2:PyString_AS_STRING>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_AS_STRING>`

.. c:function:: PyBytes_AsStringAndSize

    | Python 2: :c:func:`PyString_AsStringAndSize <py2:PyString_AsStringAndSize>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_AsStringAndSize>`

.. c:function:: PyBytes_Concat

    | Python 2: :c:func:`PyString_Concat <py2:PyString_Concat>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_Concat>`

.. c:function:: PyBytes_ConcatAndDel

    | Python 2: :c:func:`PyString_ConcatAndDel <py2:PyString_ConcatAndDel>`
    | Python 3: :c:func:`(provided) <py3:PyBytes_ConcatAndDel>`

.. c:function:: _PyBytes_Resize

    | Python 2: :c:func:`_PyString_Resize <py2:_PyString_Resize>`
    | Python 3: :c:func:`(provided) <py3:_PyBytes_Resize>`


.. index:: PyInt

PyInt
~~~~~

.. c:var:: PyInt_Type

    | Python 2: :c:data:`(provided) <py2:PyInt_Type>`
    | Python 3: :c:data:`PyLong_Type <py3:PyLong_Type>`

.. c:function:: PyInt_Check

    | Python 2: :c:func:`(provided) <py2:PyInt_Check>`
    | Python 3: :c:func:`PyLong_Check <py3:PyLong_Check>`

.. c:function:: PyInt_CheckExact

    | Python 2: :c:func:`(provided) <py2:PyInt_CheckExact>`
    | Python 3: :c:func:`PyLong_CheckExact <py3:PyLong_CheckExact>`

.. c:function:: PyInt_FromString

    | Python 2: :c:func:`(provided) <py2:PyInt_FromString>`
    | Python 3: :c:func:`PyLong_FromString <py3:PyLong_FromString>`

.. c:function:: PyInt_FromLong

    | Python 2: :c:func:`(provided) <py2:PyInt_FromLong>`
    | Python 3: :c:func:`PyLong_FromLong <py3:PyLong_FromLong>`

.. c:function:: PyInt_FromSsize_t

    | Python 2: :c:func:`(provided) <py2:PyInt_FromSsize_t>`
    | Python 3: :c:func:`PyLong_FromSsize_t <py3:PyLong_FromSsize_t>`

.. c:function:: PyInt_FromSize_t

    | Python 2: :c:func:`(provided) <py2:PyInt_FromSize_t>`
    | Python 3: :c:func:`PyLong_FromSize_t <py3:PyLong_FromSize_t>`

.. c:function:: PyInt_AsLong

    | Python 2: :c:func:`(provided) <py2:PyInt_AsLong>`
    | Python 3: :c:func:`PyLong_AsLong <py3:PyLong_AsLong>`

.. c:function:: PyInt_AS_LONG

    | Python 2: :c:func:`(provided) <py2:PyInt_AS_LONG>`
    | Python 3: :c:func:`PyLong_AS_LONG <py3:PyLong_AS_LONG>`

.. c:function:: PyInt_AsUnsignedLongLongMask

    | Python 2: :c:func:`(provided) <py2:PyInt_AsUnsignedLongLongMask>`
    | Python 3: :c:func:`PyLong_AsUnsignedLongLongMask <py3:PyLong_AsUnsignedLongLongMask>`

.. c:function:: PyInt_AsSsize_t

    | Python 2: :c:func:`(provided) <py2:PyInt_AsSsize_t>`
    | Python 3: :c:func:`PyLong_AsSsize_t <py3:PyLong_AsSsize_t>`


Module Initialization
~~~~~~~~~~~~~~~~~~~~~

.. c:function:: MODULE_INIT_FUNC(<name>)

    Python 2::

        static PyObject *PyInit_<name>(void);
        void init<name>(void);
        void init<name>(void) { PyInit_<name>(); }
        static PyObject *PyInit_<name>(void)

    Python 3::

        PyMODINIT_FUNC PyInit_<name>(void);
        PyMODINIT_FUNC PyInit_<name>(void)

.. c:type:: PyModuleDef

    Python 2:

        .. c:member:: int m_base

            Always set this to :c:macro:`PyModuleDef_HEAD_INIT`

        .. c:member:: char *m_name

        .. c:member:: char *m_doc

        .. c:member:: Py_ssize_t m_size

            Set this to -1. (Or if your module supports :c:func:`subinterpreters <py3:Py_NewInterpreter>`, use 0)

        .. c:member:: PyMethodDef m_methods

    Python 3: :c:type:`(provided) <py3:PyModuleDef>`

.. c:macro:: PyModuleDef_HEAD_INIT

    | Python 2: ``0``
    | Python 3: :c:member:`(provided) <py3:PyModuleDef.m_base>`


.. c:function:: PyModule_Create(def)

    | Python 2: :c:func:`Py_InitModule3 <py2:Py_InitModule3>`\(def->m_name, def->m_methods, def->m_doc)
    | Python 3: :c:func:`(provided) <py3:PyModule_Create>`


Types
~~~~~

.. c:macro:: Py_TPFLAGS_HAVE_WEAKREFS

    | Python 2: :c:data:`(provided) <py2:Py_TPFLAGS_HAVE_WEAKREFS>`
    | Python 3: ``0``

.. c:macro:: Py_TPFLAGS_HAVE_ITER

    | Python 2: :c:data:`(provided) <py2:Py_TPFLAGS_HAVE_ITER>`
    | Python 3: ``0``



Comparison Helpers
==================

::

    #include <py3c/comparison.h>  // (included in <py3c.h>)


.. c:macro:: Py_RETURN_NOTIMPLEMENTED

    Backported from :c:macro:`Python 3.4 <py3:Py_RETURN_NOTIMPLEMENTED>`
    for older versions

.. c:function:: PY3C_RICHCMP(val1, val2, int op)

    ::

        ((op) == Py_EQ) ? PyBool_FromLong((val1) == (val2)) : \
        ((op) == Py_NE) ? PyBool_FromLong((val1) != (val2)) : \
        ((op) == Py_LT) ? PyBool_FromLong((val1) < (val2)) : \
        ((op) == Py_GT) ? PyBool_FromLong((val1) > (val2)) : \
        ((op) == Py_LE) ? PyBool_FromLong((val1) <= (val2)) : \
        ((op) == Py_GE) ? PyBool_FromLong((val1) >= (val2)) : \
        (Py_INCREF(Py_NotImplemented), Py_NotImplemented)
