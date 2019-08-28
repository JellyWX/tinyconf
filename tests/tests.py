import sys
sys.path.append("..") # Adds higher directory to python modules path.

import tinyconf
from tinyconf.deserializers import *
from tinyconf.fields import *

import unittest

class FieldTester(unittest.TestCase):
    def assertDoesntRaise(self, proc):
        try:
            proc()
        except Exception as e:
            self.fail(f"{proc.__repr__()} raised {e.__repr__()}")

    def setUp(self):
        class TestDeserialize(Deserializer):
            integer = IntegerField()
            float_ = FloatField('float')
            string = Field('string')
            list_a = ListField('list')
            list_b = ListField('differentlist', delimiter=';')

    def testField(self):
        field = Field("test")

        self.assertEqual(field.name, "test")
        self.assertFalse(field._strict)
        self.assertTrue(field._default is None)

        field.value = "hello world"

        self.assertEqual(field.value, field._value, "hello world")

        field.value = None
        field._default = "test"

        self.assertEqual(field.value, "test")
        self.assertTrue(field._value is None)

    def testStrict(self):
        field = Field("test", strict=True)

        self.assertRaises(Field.MissingFieldData, field.validate)

        field._value = "t"
        self.assertDoesntRaise(field.validate)

        self.assertEqual(field.value, "t")

    def testInteger(self):
        field = IntegerField("test")

        field.value = "t"

        self.assertRaises(IntegerField.InvalidInteger, field.validate)

        field.value = "14"

        self.assertDoesntRaise(field.validate)
        self.assertEqual(field.value, 14)

        field.value = "14.7"

        self.assertRaises(IntegerField.InvalidInteger, field.validate)
        self.assertTrue(field.value is None)

unittest.main(verbosity=2)