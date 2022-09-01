import decimal
import unittest

from make_bst import get_sorter_for_type
from sorters import IntegerSorter, FloatSorter, CharSorter


class GetSorterForTypeTestCase(unittest.TestCase):
    """
    We use get_sorter_for_type function to pass the correct sorter to BinarySearchTreeNode instances,
    so here we ensure this work properly.
    """

    def test_receive_integer_sorter(self):
        self.assertEqual(get_sorter_for_type(int), IntegerSorter)

    def test_receive_float_sorter(self):
        self.assertEqual(get_sorter_for_type(float), FloatSorter)

    def test_receive_char_sorter(self):
        self.assertEqual(get_sorter_for_type(str), CharSorter)

    def test_unsupported_type_receive_none(self):
        self.assertEqual(get_sorter_for_type(decimal.Decimal), None)
