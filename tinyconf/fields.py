import typing

class Field():
    """Field type that deserializes directly into a :class:`str`

    Parameters
    ----------
        name: Optional[:class:`str`]
            The name of the field within the config. If not provided, uses
            the attribute name from within the :class:`Deserializer`
        strict: :class:`bool`
            Whether the field is strictly required. Defauls to ``False``
            Will cause deserialization to raise :class:`MissingFieldData`
            if an item is missing
        default:
            Specify a default value if the config doesn't specify one
    """

    class MissingFieldData(Exception):
        """Exception for when a field marked as strict is set as ``None``

        """
        pass

    def __init__(self, name: typing.Optional[str]=None, *, strict: bool=False, default: typing.Any=None, **kwargs):
        self.name: typing.Optional[str] = name
        self._value: typing.Optional[str] = None
        self._default: typing.Any = default
        self._strict: bool = strict

        self._type_specific_setup(**kwargs)

    @property
    def value(self) -> typing.Optional[str]:
        """Used during deserialization

        """
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    def validate(self):
        """Used during deserialization to determine if there are any issues with
        a field's contents

        """
        if self._value is None and self._strict:
            raise self.MissingFieldData
        elif self._value is None and self._default is not None:
            self._value = self._default
        elif self._value is not None:
            self._type_specific_validation()

    def _type_specific_validation(self):
        pass

    def _type_specific_setup(self, **kwargs):
        pass


class IntegerField(Field):
    """Field derivative that deserializes an integer

    """
    class InvalidInteger(Exception):
        """Exception raised when the field contents are not a valid integer

        """
        pass

    def _type_specific_validation(self):
        if not all([x in '-0123456789' for x in self._value]):
            raise self.InvalidInteger

    @Field.value.getter
    def value(self) -> typing.Optional[int]:
        return None if self._value is None else int(self._value)


class FloatField(Field):
    """Field derivative that deserializes a floating point value

    """
    class InvalidFloat(Exception):
        """Exception raised when the field contents are not a valid float

        """
        pass

    def _type_specific_validation(self):
        if not all([x in '-.0123456789' for x in self._value]):
            raise self.InvalidFloat

    @Field.value.getter
    def value(self) -> typing.Optional[int]:
        return None if self._value is None else float(self._value)


class ListField(Field):
    """Field derivative that deserializes a list value

    Parameters
    ----------
        delimiter: :class:`str`
            Specifies the list delimiter. Defaults to ``","``
        remove_blank: :class:`bool`
            Specifies if empty list items should be removed. Defaults to ``False``
    """
    def _type_specific_setup(self, delimiter: str=',', remove_blank: bool=False):
        self.delimiter = delimiter
        self.remove_blank = remove_blank

    @Field.value.getter
    def value(self) -> typing.Optional[list]:
        if self.remove_blank:
            return None if self._value is None else [x for x in self._value.split(self.delimiter) if bool(x)]

        else:
            return None if self._value is None else self._value.split(self.delimiter)