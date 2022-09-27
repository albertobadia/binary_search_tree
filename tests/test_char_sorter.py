from errors import InvalidCharLenException
from sorters import CharSorter
from tests.base_sorter_testcase import BaseSorterTestCase


class CharSorterTestCase(BaseSorterTestCase.TestCase):
    """
    Tests collection for CharSorterUseCases
    """
    sorter = CharSorter
    correct_value_lower = "a"
    correct_value_bigger = "x"
    incorrect_value = 1

    def test_receive_string_not_char(self):
        """
        CharSorter special case, we are expecting to receive a string of length 1
        """
        with self.assertRaises(InvalidCharLenException):
            self.sorter.is_lower_than("aaa", "b")
