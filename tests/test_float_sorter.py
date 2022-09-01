from sorters import FloatSorter
from tests.base_sorter_testcase import BaseSorterTestCase


class FloatSorterTestCase(BaseSorterTestCase.TestCase):
    """
    Tests collection for IntegerSorterUseCases
    """

    sorter = FloatSorter
    allowed_type = float
    correct_value_lower = 0.1
    correct_value_bigger = 2.5
