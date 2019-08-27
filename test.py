from tinyconf import *
from tinyconf.fields import *

class ini(IniDeserializer):
    __filename__ = 'test.ini'

    integer = IntegerField()
    float_ = FloatField('float')
    string = Field('string')
    list_a = ListField('list')
    list_b = ListField('differentlist', delimiter=';')

a = ini()