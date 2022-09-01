from sorters import IntegerSorter
from tests.base_sorter_testcase import BaseSorterTestCase


class IntegerSorterTestCase(BaseSorterTestCase.TestCase):
    """
    Tests collection for IntegerSorterUseCases
    """

    sorter = IntegerSorter
    allowed_type = int
    correct_value_lower = 1
    correct_value_bigger = 99
