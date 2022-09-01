"""
Here we write "sorters" functions to be used from binary search trees.
The only goal of this functions is to check if a value is considered lower than other.
So there should a sorter for every data type that you want to store on the
binary search trees.
"""
import typing

from errors import InvalidCharLenException, InvalidTypeException, EqualValuesException


class BaseSorter:
    """
    This class acts as a contract to define binary search tree sorters,
    we put here some common logic.
    """

    allowed_type: typing.Type = None

    @classmethod
    def validate_values(cls, a, b):
        """
        Validate values before compare
        """
        # Check if values are allowed type
        if not isinstance(a, cls.allowed_type) or not isinstance(b, cls.allowed_type):
            raise InvalidTypeException(f"We allow {cls.allowed_type} value types only.")

        # If we have the same value, the comparator will not work properly
        if a == b:
            raise EqualValuesException(f"Both values are equal.")

    @classmethod
    def is_lower_than(cls, a, b) -> bool:
        """
        Check if first value is considered lower than the second
        """
        cls.validate_values(a, b)  # Validate values
        return a < b


class IntegerSorter(BaseSorter):
    allowed_type = int


class FloatSorter(BaseSorter):
    allowed_type = float


class CharSorter(BaseSorter):
    """
    Note that this sorter requires some extra behavior to compare / validate values
    """

    allowed_type = str

    @classmethod
    def validate_values(cls, a: str, b: str):
        super().validate_values(a, b)
        # Validate it's a char (string of length 1)
        if len(a) > 1 or len(b) > 1:
            raise InvalidCharLenException("We only accept string of length 1.")

    @classmethod
    def is_lower_than(cls, a: str, b: str) -> bool:
        """Special handling for chars, we have to do some extra work"""
        try:  # <- we do this extra validation here to be sure equal chars match
            _a = a.lower()
            _b = b.lower()
        except AttributeError:
            # Re launch correct exception when found other type
            raise InvalidTypeException("We only accept chars here.")

        cls.validate_values(_a, _b)
        # In this case, we compare both by getting the unicode number of the char
        return ord(_a) < ord(_b)
