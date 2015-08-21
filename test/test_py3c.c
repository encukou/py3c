#include <Python.h>
#include <py3c.h>

#define UTF8_STRING "test string \xe1\xba\x87\xc3\xad\xc5\xa5\xc4\xa7 \xc5\xae\xc5\xa2\xe1\xb8\x9e\xe2\x88\x9e \xe2\x98\xba"
#define FORMAT_STRING "<%s:%d>"

static PyObject *str_check(PyObject *mod, PyObject * o) {
	return PyBool_FromLong(PyStr_Check(o));
}

static PyObject *str_checkexact(PyObject *mod, PyObject * o) {
	return PyBool_FromLong(PyStr_CheckExact(o));
}

static PyObject *str_fromstring(PyObject *mod) {
	return PyStr_FromString(UTF8_STRING);
}

static PyObject *str_fromstringandsize(PyObject *mod, PyObject * o) {
	return PyStr_FromStringAndSize(UTF8_STRING, PyInt_AsLong(o));
}

static PyObject *str_fromformat(PyObject *mod) {
	return PyStr_FromFormat(FORMAT_STRING, "abc", 3);
}

static PyObject *_fromformatv(char *fmt, ...) {
	va_list valist;
	va_start(valist, fmt);
	return PyStr_FromFormatV(fmt, valist);
}

static PyObject *str_fromformatv(PyObject *mod) {
	return _fromformatv(FORMAT_STRING, "abc", 3);
}

static PyObject *str_asstring_check(PyObject *mod, PyObject * o) {
	char *str = PyStr_AsString(o);
	if (!str) return NULL;
	return PyBool_FromLong(!strcmp(str, UTF8_STRING));
}

static PyObject *str_concat(PyObject *mod, PyObject *args) {
	PyObject *left, *right;
	if (!PyArg_ParseTuple(args, "OO", &left, &right)) return  NULL;
	return PyStr_Concat(left, right);
}

static PyObject *str_format(PyObject *mod, PyObject *args) {
	PyObject *fmt, *items;
	if (!PyArg_ParseTuple(args, "OO", &fmt, &items)) return  NULL;
	return PyStr_Format(fmt, items);
}

static PyObject *str_interninplace(PyObject *mod, PyObject *o) {
	PyStr_InternInPlace(&o);
	return o;
}

static PyObject *str_internfromstring(PyObject *mod) {
	return PyStr_InternFromString(UTF8_STRING);
}

static PyObject *str_decode(PyObject *mod, PyObject *args) {
	int size;
	const char *errors;
	if (!PyArg_ParseTuple(args, "Is", &size, &errors)) return  NULL;
	return PyStr_Decode(UTF8_STRING, size, "utf-8", errors);
}

static PyObject *str_asutf8string(PyObject *mod, PyObject *o) {
	return PyStr_AsUTF8String(o);
}

static PyObject *str_asutf8_check(PyObject *mod, PyObject * o) {
	char *str = PyStr_AsUTF8(o);
	if (!str) return NULL;
	return PyBool_FromLong(!strcmp(str, UTF8_STRING));
}

static PyObject *str_asutf8andsize_check(PyObject *mod, PyObject * o) {
	Py_ssize_t size;
	char *str = PyStr_AsUTF8AndSize(o, &size);
	if (!str) return NULL;
	return PyBool_FromLong(!strcmp(str, UTF8_STRING) && size == 36);
}

#define FUNC(style, name) { #name, (PyCFunction)name, style, NULL }

static PyMethodDef methods[] = {
	FUNC(METH_O, str_check),
	FUNC(METH_O, str_checkexact),
	FUNC(METH_NOARGS, str_fromstring),
	FUNC(METH_O, str_fromstringandsize),
	FUNC(METH_NOARGS, str_fromformat),
	FUNC(METH_NOARGS, str_fromformatv),
	FUNC(METH_O, str_asstring_check),
	FUNC(METH_VARARGS, str_concat),
	FUNC(METH_VARARGS, str_format),
	FUNC(METH_O, str_interninplace),
	FUNC(METH_O, str_internfromstring),
	FUNC(METH_VARARGS, str_decode),
	FUNC(METH_O, str_asutf8string),
	FUNC(METH_O, str_asutf8_check),
	FUNC(METH_O, str_asutf8andsize_check),
	{ NULL }
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    .m_name = "test_py3c",
    .m_doc = PyDoc_STR("Testing module for py3c."),
    .m_size = -1,
    .m_methods = methods,
};

MODULE_INIT_FUNC(test_py3c)
{
	PyObject *m = PyModule_Create(&moduledef);

	if (PyModule_AddObject(m, "str_type", (PyObject *)&PyStr_Type)) goto error;
	Py_INCREF(&PyStr_Type);

    return m;

error:
	return NULL;
}
