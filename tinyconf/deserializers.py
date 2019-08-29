import typing
from io import IOBase

import os
import configparser
from configparser import ConfigParser

from tinyconf.fields import Field
from tinyconf.section import Section

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
            Which section should be loaded. Default is ``None``. If ``None``, will
            load sections based on :class:`tinyconf.section.Section` objects within model.
        **kwargs:
            All other named arguments are passed to the underlying :class:`ConfigParser`

    """

    def __init__(self, *args,
        file: typing.Optional[IOBase]=None,
        filename: typing.Optional[str]=None,
        string: str='',
        section: typing.Optional[str]=None,
        **kwargs):

        cp = ConfigParser(*args, **kwargs)
        if file is not None:
            cp.read_file(file)
        elif filename is not None:
            with open(filename, 'r') as f:
                cp.read_file(f)
        else:
            cp.read_string(string)

        if section is not None:
            data: dict = dict(cp[section])
            self._deserialize(data)
        else:
            self._deserialize_sections(cp)


    def _deserialize_sections(self, cp: ConfigParser):
        for attrib in dir(self):
            section = getattr(self, attrib)
            if isinstance(section, Section):
                for field in section.contents:
                    field.section = section.name or attrib

        for attrib in dir(self):
            d = getattr(self, attrib)
            if isinstance(d, Field):
                if d.section is not None:
                    # Get the attribute from the data
                    try:
                        v: typing.Optional[str] = cp.get(d.section, d.name or attrib)
                    except configparser.NoOptionError:
                        v: typing.Optional[str] = None

                    d.value = v

                    # Check the value is valid
                    d.validate()

                    # Finally, rebind to the value of the field
                    self.__dict__[attrib] = d.value

                else:
                    d.value = None

                    d.validate()

                    self.__dict__[attrib] = d.value


class EnvDeserializer(Deserializer):
    """Deserializes from the operating system environment variables

    """
    def __init__(self, *args, **kwargs):
        self._deserialize(dict(os.environ))
