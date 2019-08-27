import typing

class Field():
    class FieldLengthExceeded(Exception):
        pass

    class MissingFieldData(Exception):
        pass

    def __init__(self, name: str, *, strict: bool=False, max_length: int=1024, **kwargs):
        self.name: str = name
        self._value: typing.Optional[str] = None
        self._strict: bool = strict
        self._max_length: int = max_length

        self._type_specific_setup(**kwargs)

    @property
    def value(self) -> typing.Optional[str]:
        return self._value
    
    @value.setter
    def value(self, value):
        if value is not None and len(value) > self._max_length:
            raise self.FieldLengthExceeded
        else:
            self._value = value

    def validate(self):
        if self._value is None and self._strict:
            raise self.MissingFieldData
        elif self._value is not None:
            self._type_specific_validation()

    def _type_specific_validation(self):
        pass

    def _type_specific_setup(self, **kwargs):
        pass


class IntegerField(Field):
    class InvalidInteger(Exception):
        pass

    def _type_specific_validation(self):
        if not all([x in '-0123456789' for x in self._value]):
            raise self.InvalidInteger

    @Field.value.getter
    def value(self) -> typing.Optional[int]:
        return None if self._value is None else int(self._value)


class FloatField(Field):
    class InvalidFloat(Exception):
        pass

    def _type_specific_validation(self):
        if not all([x in '-.0123456789' for x in self._value]):
            raise self.InvalidFloat

    @Field.value.getter
    def value(self) -> typing.Optional[int]:
        return None if self._value is None else float(self._value)


class ListField(Field):
    def _type_specific_setup(self, delimiter: str=',', remove_blank: bool=False):
        self.delimiter = delimiter
        self.remove_blank = remove_blank

    @Field.value.getter
    def value(self) -> typing.Optional[list]:
        if self.remove_blank:
            return None if self._value is None else [x for x in self._value.split(self.delimiter) if bool(x)]

        else:
            return None if self._value is None else self._value.split(self.delimiter)