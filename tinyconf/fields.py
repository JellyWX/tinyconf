import typing
import types


class Field:
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
            Specify a default value if the config doesn't specify a value,
            or the value specified fails validation.

    Attributes
    ----------
        valid: :class:`bool`
            If the field data is valid
        name:
            The name of the field (if specified)

    """

    class MissingFieldData(Exception):
        """Exception for when a field marked as strict is set as ``None``

        """
        pass

    def __init__(self, name: typing.Optional[str] = None, *, strict: bool = False, default: typing.Any = None,
                 **kwargs):
        self.name: typing.Optional[str] = name
        self.valid: bool = True
        self._value: typing.Optional[str] = None
        self._default: typing.Any = default
        self._strict: bool = strict
        self.section = None

        self._type_specific_setup(**kwargs)

    @property
    def value(self) -> typing.Optional[str]:
        """Used during deserialization

        """
        if self._value is None or not self.valid:
            return self._default

        else:
            return self._type_specific_process(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    def validate(self):
        """Used during deserialization to determine if there are any issues with
        a field's contents

        """
        self.valid = True

        if self._value is None and self._strict:
            self.valid = False
            raise self.MissingFieldData

        elif self._value is not None:
            self._type_specific_validation()

    def _type_specific_validation(self):
        pass

    def _type_specific_setup(self, **kwargs):
        pass

    def _type_specific_process(self, val: str) -> str:
        return val


class IntegerField(Field):
    """Field derivative that deserializes an integer

    """

    class InvalidInteger(Exception):
        """Exception raised when the field contents are not a valid integer

        """
        pass

    def _type_specific_validation(self):
        if not all([x in '-0123456789' for x in self._value]):
            self.valid = False
            raise self.InvalidInteger

    def _type_specific_process(self, val: str) -> int:
        return int(val)


class FloatField(Field):
    """Field derivative that deserializes a floating point value

    """

    class InvalidFloat(Exception):
        """Exception raised when the field contents are not a valid float

        """
        pass

    def _type_specific_validation(self):
        if not all([x in '-.0123456789' for x in self._value]):
            self.valid = False
            raise self.InvalidFloat

    def _type_specific_process(self, val: str) -> float:
        return float(val)


class BooleanField(Field):
    """Field derivative that deserializes some sort of boolean value

    Parameters
    ----------
        comparators: List[:class:`str`]
            Specifies what the value should be compared with. Defaults to ['1', 'y', 'yes', 't', 'true']

    """

    def _type_specific_setup(self,
                             comparators: typing.List[str] = ['1', 'y', 'yes', 't', 'true']):
        self._comparators = comparators

    def _type_specific_process(self, val: str) -> bool:
        if val in self._comparators:
            return True
        else:
            return False


class ListField(Field):
    """Field derivative that deserializes a list value

    Parameters
    ----------
        delimiter: :class:`str`
            Specifies the list delimiter. Defaults to ``","``
        filter: Optional[:class:`FunctionType`]
            Specifies a filtering function to be applied to the contents.
            Default ``lambda x: True``
        map: Optional[:class:`FunctionType`]
            Specifies a function to map across every element.
            Default ``lambda x: x``

    """

    def _type_specific_setup(self,
                             delimiter: str = ',',
                             filter: types.FunctionType = lambda x: True,
                             map: types.FunctionType = lambda x: x):
        self._delimiter: str = delimiter
        self._filter: types.FunctionType = filter
        self._map: types.FunctionType = map

    def _type_specific_process(self, val: str) -> list:
        return [self._map(x) for x in self._value.split(self._delimiter) if self._filter(x)]
