import typing
from io import IOBase

import os
from configparser import ConfigParser

from tinyconf.fields import Field

class Deserializer():
    """Base class for deserializers

    """
    def _deserialize(self, data: dict):
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
    
    Parameters
    ----------
        *args:
            All unnamed arguments are passed to the underlying :class:`ConfigParser`
        filename: Optional[:class:`str`]
            Load a file object by name as a config file
        file: Optional[:class:`IOBase`]
            Load a file object as a config file. Please note- the file will not be
            automatically closed.
        string: Optional[:class:`str`]
            Load a string as a config file
        section: Optional[:class:`str`]
            Which section should be loaded. Default is ``"DEFAULT"``
        **kwargs:
            All other named arguments are passed to the underlying :class:`ConfigParser`

    """

    def __init__(self, *args,
        file: typing.Optional[IOBase]=None,
        filename: typing.Optional[str]=None,
        string: str='',
        section='DEFAULT',
        **kwargs):

        cp = ConfigParser(*args, **kwargs)
        if file is not None:
            cp.read_file(file)
        elif filename is not None:
            with open(filename, 'r') as f:
                cp.read_file(f)
        else:
            cp.read_string(string)

        data: dict = dict(cp[section])
        else:
            self._deserialize(data)

class EnvDeserializer(Deserializer):
    """Deserializes from the operating system environment variables

    """
    def __init__(self, *args, **kwargs):
        self._deserialize(dict(os.environ))
