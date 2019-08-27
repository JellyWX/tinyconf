import typing
from tinyconf.fields import Field
from configparser import ConfigParser

class Deserializer():
    """Base class for deserializers

    """
    def deserialize(self, data: dict):
        """Deserializes `data`.

        :param data: Dictionary of values to be deserialized
        :type data: dict

        """
        for attrib in dir(self):
            d = getattr(self, attrib)
            if isinstance(d, Field):
                # Get the attribute from the data
                v: typing.Optional[str] = data.get(d.name or attrib, None)

                d.value = v

                # Check the value is valid
                d.validate()

                # Finally, rebind to the value of the field
                self.__dict__[attrib] = d.value

class IniDeserializer(Deserializer):
    """Class representing a deserializer for an INI file.
    
    Attributes
    ----------
        __filename__: Optional[:class:`str`]
            Name of the file to be loaded

        __config__: Optional[:class:`str`]
            Raw string of ini-formatted data to be loaded. Either this or
            ``__filename__`` must be defined
    """
    class NoConfig(Exception):
        """Raised when both ``__filename__`` and ``__config__`` are missing.

        """
        pass

    def __init__(self):
        cp = ConfigParser()
        try:
            cp.read_file(open(self.__filename__, 'r'))
        except NameError:
            try:
                cp.read_string(self.__config__)
            except NameError:
                raise self.NoConfig

        for _, section in cp.items():
            self.deserialize(section)