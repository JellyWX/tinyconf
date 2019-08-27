import typing
from tinyconf.fields import Field
from configparser import ConfigParser

class Deserializer():
    def deserialize(self, data: dict):
        for attrib in dir(self):
            d = getattr(self, attrib)
            if isinstance(d, Field):
                # Get the attribute from the form data
                v: typing.Optional[str] = data.get(d.name, None)

                d.value = v

                # Check the value is valid
                d.validate()

                # Finally, rebind to the value of the field
                self.__dict__[attrib] = d.value

class IniDeserializer(Deserializer):
    def __init__(self):
        cp = ConfigParser()
        cp.read_file(open(self.__filename__, 'r'))

        for _, section in cp.items():
            self.deserialize(section)