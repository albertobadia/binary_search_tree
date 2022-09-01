import decimal
import unittest

from errors import MultipleDataTypesException, TypeSorterNotFoundException
from make_bst import make_binary_search_tree
from sorters import CharSorter


class MakeBinarySearchTreeTestCase(unittest.TestCase):
    """
    We use make_binary_search_tree function to get correct sorter for values type,
    validate that all are the same type, create root node, and propagate values addition.
    """

    def test_multiple_data_types_exception(self):
        """
        If we call it with different data type values, should raise a MultipleDataTypesException .
        """
        with self.assertRaises(MultipleDataTypesException):
            make_binary_search_tree(values=["a", 1])

    def test_type_sorter_not_found_exception(self):
        """
        Here we ensure that unsupported data type value raises TypeSorterNotFoundException
        """
        with self.assertRaises(TypeSorterNotFoundException):
            make_binary_search_tree(values=[decimal.Decimal("1"), decimal.Decimal("2")])

    def test_sorter_setup_properly(self):
        """
        The function should receive the correct sorter from get_sorter_from_type, here ensure we call it.
        """
        char_bst = make_binary_search_tree(values=["a", "b", "c"])
        self.assertEqual(char_bst.sorter, CharSorter)

    def test_root_node_is_first_value(self):
        """
        Root node should always have the first given value
        """
        char_bst = make_binary_search_tree(values=["a", "b", "c"])
        self.assertEqual(char_bst.node_value, "a")
