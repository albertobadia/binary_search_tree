import typing

from binary_search_tree import BinarySearchTreeNode
from errors import MultipleDataTypesException, TypeSorterNotFoundException
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

    data_type = set([type(i) for i in values])
    if len(data_type) > 1:  # <- Validate that we receive all values same type
        raise MultipleDataTypesException("We receive different type values")
    data_type = data_type.pop()

    sorter = get_sorter_for_type(data_type)  # <- get the sorter for that type
    if sorter is None:
        raise TypeSorterNotFoundException(f"Sorter for type {data_type}.")

    root_node = BinarySearchTreeNode(sorter=sorter, node_value=values[0])
    if len(values) > 1:
        root_node.add_multiple(values[1:])

    return root_node
