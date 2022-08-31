"""
Here we write "sorters" functions to be used from binary search trees.
The only goal of this functions is to check if a value is considered lower than other.
So there should a sorter for every data type that you want to store on the
binary search trees.
"""
import typing


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
            raise TypeError(f'We allow {cls.allowed_type} value types only.')

        # If we have the same value, the comparator will not work properly
        if a == b:
            raise ValueError(f'Both values are equal.')

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
