import typing

from binary_search_tree import BinarySearchTreeNode
from errors import MultipleDataTypesException, TypeSorterNotFoundException, InvalidTypeException
from sorters import BaseSorter, IntegerSorter, CharSorter, FloatSorter


def get_sorter_for_type(_type: typing.Type) -> typing.Type[BaseSorter]:
    """Gets the sorter that corresponds to given type"""
    types_to_sorters_map = {
        int: IntegerSorter,
        float: FloatSorter,
        str: CharSorter,
    }
    return types_to_sorters_map.get(_type)


def make_binary_search_tree(values: list[typing.Any]) -> BinarySearchTreeNode:
    """Build a BinarySearchTree instance from given values arguments"""

    try:
        data_type = type(values[0])
        sorter = get_sorter_for_type(data_type)
        if sorter is None:
            raise TypeSorterNotFoundException(f"Sorter for type {data_type}.")

        root_node = BinarySearchTreeNode(sorter=sorter, node_value=values[0])
        if len(values) > 1:
            root_node.add_multiple(values[1:])

        return root_node

    except InvalidTypeException:
        raise MultipleDataTypesException('We receive different data types on input.')
