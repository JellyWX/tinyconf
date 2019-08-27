import sys
sys.path.append("..") # Adds higher directory to python modules path.

import tinyconf
from tinyconf.deserializers import *
from tinyconf.fields import *

import unittest

class DeserializeTester(unittest.TestCase):
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
        field.validate()

        self.assertEqual(field.value, "t")

unittest.main(verbosity=2)