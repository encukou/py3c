# encoding: UTF-8

import unittest
import sys
import operator

import test_py3c

PY3 = sys.version_info >= (3, 0)
PY2 = not PY3

TEXT_STRING = 'test string ' + 'ẇíťħ ŮŢḞ∞ ☺'

if PY3:
    intern = sys.intern


class StringSubclass(str): pass
class IntSubclass(int): pass


class TestCase(unittest.TestCase):
    if sys.version_info < (2, 7):
        def assertIs(self, left, right):
            self.assertTrue(left is right)


class StringChecks(TestCase):
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


class IntChecks(TestCase):
    def test_type(self):
        self.assertIs(test_py3c.int_type, int)

    def test_check(self):
        self.assertTrue(test_py3c.int_check(8))
        self.assertFalse(test_py3c.int_check("abc"))
        self.assertTrue(test_py3c.int_check(IntSubclass()))
        self.assertEqual(test_py3c.int_check(2**1000), PY3)

    def test_check_exact(self):
        self.assertTrue(test_py3c.int_checkexact(8))
        self.assertFalse(test_py3c.int_checkexact("abc"))
        self.assertFalse(test_py3c.int_checkexact(IntSubclass()))
        self.assertEqual(test_py3c.int_checkexact(2**1000), PY3)

    def test_from(self):
        self.assertEqual(test_py3c.int_fromstring(), 8)
        self.assertEqual(test_py3c.int_fromlong(), 8)
        self.assertEqual(test_py3c.int_fromssize_t(), 8)
        self.assertEqual(test_py3c.int_fromsize_t(), 8)

    def test_as(self):
        self.assertTrue(test_py3c.int_aslong_check(8))
        self.assertTrue(test_py3c.int_aslong_macro_check(8))
        self.assertTrue(test_py3c.int_asunsignedlonglongmask_check(8))
        self.assertTrue(test_py3c.int_asssize_t_check(8))


class TypeChecks(TestCase):
    def test_return_notimplemented(self):
        self.assertIs(test_py3c.return_notimplemented(), NotImplemented)

    def test_number(self):
        num = test_py3c.Number(3)
        self.assertEqual(num.value, 3)
        num.value = 5
        self.assertEqual(num.value, 5)

    def test_number_number_equality(self):
        three = test_py3c.Number(3)
        three2 = test_py3c.Number(3)
        five = test_py3c.Number(5)
        self.assertEqual(three, three)
        self.assertEqual(three, three2)
        self.assertNotEqual(three, five)

    def test_number_int_equality(self):
        three = test_py3c.Number(3)
        five = test_py3c.Number(5)
        self.assertEqual(three, 3)
        self.assertNotEqual(three, 5)

    def test_all_comparisons(self):
        three = test_py3c.Number(3)
        three2 = test_py3c.Number(3)
        five = test_py3c.Number(5)
        for op in (operator.eq, operator.ne, operator.gt, operator.lt,
                   operator.ge, operator.le):
            self.assertEqual(op(three, three), op(3, 3))
            self.assertEqual(op(three, three2), op(3, 3))
            self.assertEqual(op(three, five), op(3, 5))
            self.assertEqual(op(five, three), op(5, 3))

            self.assertEqual(op(three, 3), op(3, 3))
            self.assertEqual(op(3, three), op(3, 3))
            self.assertEqual(op(three, 5), op(3, 5))
            self.assertEqual(op(5, three), op(5, 3))


if __name__ == '__main__':
    unittest.main()
