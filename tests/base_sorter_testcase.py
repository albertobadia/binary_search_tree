import typing
import unittest

from errors import InvalidTypeException, EqualValuesException
from sorters import BaseSorter


class BaseSorterTestCase:
    """
    We put the tests class inside a parent class to avoid be detected by test runners
    """

    class TestCase(unittest.TestCase):
        """
        Common tests collection for sorters use cases
        """

        sorter = BaseSorter  # <- Sorter that we are testing
        allowed_type = typing.Type  # <- Type that the test should check for
        correct_value_lower = 1  # <- An example of a correct value
        correct_value_bigger = 2  # <- An example of bigger correct value
        incorrect_value = "a"  # <- An example of an incorrect value

        def test_invalid_type_exception(self):
            """
            Every sorter has an property called 'allowed_type', received values should be the same type.
            In case not, we raise InvalidTypeException error, other controllers depends from that approach to run well.
            """

            with self.assertRaises(InvalidTypeException):
                self.sorter.validate_values(
                    self.incorrect_value, self.correct_value_lower
                )

        def test_equal_values_exception(self):
            """
            We should raise if receive two equal values, it should be handled from parent business controller.
            """
            with self.assertRaises(EqualValuesException):
                self.sorter.validate_values(
                    self.correct_value_lower, self.correct_value_lower
                )

        def test_compare_pre_validate_values(self):
            """
            Maybe an accident, maybe is in the dna, but every programmer hate at least one validator.
            Here we create the public enemy, a validator for a validator, take that inception.

            NOTE: we check that the validations run
            """
            with self.assertRaises(InvalidTypeException):
                self.sorter.is_lower_than(
                    self.correct_value_lower, self.incorrect_value
                )

        def test_compare_when_is_lower(self):
            """
            Calling with a < b should return True
            """
            self.assertTrue(
                self.sorter.is_lower_than(
                    self.correct_value_lower, self.correct_value_bigger
                )
            )

        def test_compare_when_is_bigger(self):
            """
            Calling with a > b should return True
            """
            self.assertFalse(
                self.sorter.is_lower_than(
                    self.correct_value_bigger, self.correct_value_lower
                )
            )
