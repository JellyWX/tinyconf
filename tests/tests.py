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

    def testDefault(self):
        field = Field(default="123")

        field.value = "t"

        self.assertEqual(field.value, "t")

        field.value = None

        self.assertEqual(field.value, "123")

        field.value = "t"
        field.valid = False

        self.assertEqual(field.value, "123")

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

    def testFloat(self):
        field = FloatField(default=0.0)

        field.value = "t"

        self.assertRaises(FloatField.InvalidFloat, field.validate)
        self.assertEqual(field.value, 0.0)

        field.value = "14"

        self.assertDoesntRaise(field.validate)
        self.assertEqual(field.value, 14)

        field.value = "14.7"

        self.assertDoesntRaise(field.validate)
        self.assertEqual(field.value, 14.7)

    def testList(self):
        field = ListField()

        field.value = "a,b,e,g"

        self.assertEqual(field.value, ['a', 'b', 'e', 'g'])

        field._filter = lambda x: x in 'ab'

        self.assertEqual(field.value, ['a', 'b'])

        field._filter = lambda x: True
        field.value = "1;2;3;4"

        self.assertEqual(field.value, ['1;2;3;4'])

        field._delimiter = ';'

        self.assertEqual(field.value, ['1', '2', '3', '4'])

        field._map = lambda x: int(x)

        self.assertEqual(field.value, [1, 2, 3, 4])

class DeserializeTester(unittest.TestCase):
    def assertDoesntRaise(self, proc):
        try:
            proc()
        except Exception as e:
            self.fail(f"{proc.__repr__()} raised {e.__repr__()}")

    def testIni(self):
        class IniTest(IniDeserializer):
            integer = IntegerField()
            float_ = FloatField('float')
            string = Field('string')
            list_a = ListField('list')
            list_b = ListField('differentlist', delimiter=';')
            filterlist = ListField(filter=lambda x: int(x) == 1, map=lambda x: int(x))

        initest = IniTest(string='''[CONTENTS]
integer=1
float=5.0
list=1,2,3,4
differentlist=1,2;3,4;ab
filterlist=1,0,1,0,1
            ''', section='CONTENTS')

        self.assertEqual(initest.integer, 1)
        self.assertEqual(initest.float_, 5.0)
        self.assertEqual(initest.list_a, ['1', '2', '3', '4'])
        self.assertEqual(initest.list_b, ['1,2', '3,4', 'ab'])
        self.assertEqual(initest.filterlist, [1, 1, 1])

    def testIni2(self):
        class Config(IniDeserializer):
            token = Field(strict=True) # Loads field called 'token'. Fails if not present

            client_id = IntegerField('client') # Loads field called 'client'

            api_version = Field('apiv', default="8") # Loads field called 'apiv', if not present uses "8"

            permitted_users = ListField(map=lambda x: int(x.strip()), default=[], delimiter=";")


        self.assertRaises(Field.MissingFieldData, lambda: Config(string=''))
        self.assertRaises(Field.MissingFieldData, lambda: Config(filename='confb.ini'))
        self.assertDoesntRaise(lambda: Config(filename='confc.ini'))

        config = Config(filename="confa.ini")

        self.assertEqual(config.token, "abcdefghijklmno")
        self.assertEqual(config.client_id, 123456789)
        self.assertEqual(config.api_version, "8")
        self.assertEqual(config.permitted_users, [1111, 2222])

unittest.main(verbosity=2)