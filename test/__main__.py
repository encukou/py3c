# encoding: UTF-8

import unittest
import sys

import test_py3c

PY3 = sys.version_info >= (3, 0)
PY2 = not PY3

TEXT_STRING = 'test string ' + 'ẇíťħ ŮŢḞ∞ ☺'

if PY3:
    intern = sys.intern


class StringSubclass(str): pass


class StringChecks(unittest.TestCase):
    def test_type(self):
        self.assertIs(test_py3c.str_type, str)

    def test_check(self):
        self.assertTrue(test_py3c.str_check("abc"))
        self.assertFalse(test_py3c.str_check(8))
        self.assertTrue(test_py3c.str_check(StringSubclass()))
        self.assertEqual(test_py3c.str_check(b"abc"), PY2)
        self.assertEqual(test_py3c.str_check(u"abc"), PY3)

    def test_check_exact(self):
        self.assertTrue(test_py3c.str_checkexact("abc"))
        self.assertFalse(test_py3c.str_checkexact(8))
        self.assertFalse(test_py3c.str_checkexact(StringSubclass()))
        self.assertEqual(test_py3c.str_check(b"abc"), PY2)
        self.assertEqual(test_py3c.str_check(u"abc"), PY3)

    def test_fromstring(self):
        self.assertEqual(test_py3c.str_fromstring(), TEXT_STRING)

    def test_fromstringandsize(self):
        self.assertEqual(test_py3c.str_fromstringandsize(11), "test string")
        self.assertEqual(test_py3c.str_fromstringandsize(36), TEXT_STRING)
        if PY2:
            self.assertEqual(test_py3c.str_fromstringandsize(13), TEXT_STRING[:13])
        else:
            self.assertRaises(UnicodeDecodeError, test_py3c.str_fromstringandsize, 13)

    def test_fromformat(self):
        self.assertEqual(test_py3c.str_fromformat(), "<abc:3>")
        self.assertEqual(test_py3c.str_fromformatv(), "<abc:3>")

    def test_asstring(self):
        self.assertTrue(test_py3c.str_asstring_check(TEXT_STRING))
        self.assertFalse(test_py3c.str_asstring_check("---"))
        self.assertRaises(TypeError, test_py3c.str_asstring_check, 8)

    def test_concat(self):
        self.assertEqual(test_py3c.str_concat(TEXT_STRING, "\0abc"), TEXT_STRING + "\0abc")
        self.assertRaises((TypeError, SystemError), test_py3c.str_concat, 8, "\0abc")

    def test_format(self):
        self.assertEqual(test_py3c.str_format("%s %d %.2f", ("a", 1, 3.5)), "a 1 3.50")
        self.assertRaises(TypeError, test_py3c.str_format, 8)
        self.assertRaises(TypeError, test_py3c.str_format, "%d", "-")

    def test_interninplace(self):
        self.assertEqual(test_py3c.str_interninplace("ab" + "cd"), intern("abcd"))

    def test_internfromstring(self):
        self.assertEqual(test_py3c.str_internfromstring(TEXT_STRING), intern(TEXT_STRING))

    def test_decode(self):
        self.assertEqual(test_py3c.str_decode(11, "strict"), "test string")
        # XXX
        #self.assertEqual(test_py3c.str_decode(36, "strict"), UTF8_STRING)
        #self.assertEqual(test_py3c.str_decode(13, "replace"), "test string \N{REPLACEMENT CHARACTER}")

    def test_asutf8string(self):
        if PY2:
            self.assertEqual(test_py3c.str_asutf8string(TEXT_STRING), TEXT_STRING)
        else:
            self.assertEqual(test_py3c.str_asutf8string(TEXT_STRING), TEXT_STRING.encode('utf-8'))

    def test_asutf8(self):
        self.assertTrue(test_py3c.str_asstring_check(TEXT_STRING))
        self.assertFalse(test_py3c.str_asstring_check("---"))
        self.assertRaises(TypeError, test_py3c.str_asstring_check, 8)


if __name__ == '__main__':
    unittest.main()
