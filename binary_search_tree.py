import dataclasses
import typing

from sorters import BaseSorter, IntegerSorter


@dataclasses.dataclass
class BinarySearchTreeNode:
    """
    This is a Binary search tree node, which has left and right child nodes of same class
    """

    sorter: typing.Type[BaseSorter]

    node_value: typing.Any

    left_node = None
    right_node = None

    def add(self, value):
        """Add single value"""

        if self.sorter.is_lower_than(value, self.node_value):

            if self.left_node is not None:
                self.left_node.add(value)
            else:
                self.left_node = BinarySearchTreeNode(sorter=self.sorter, node_value=value)

        else:

            if self.right_node is not None:
                self.right_node.add(value)
            else:
                self.right_node = BinarySearchTreeNode(sorter=self.sorter, node_value=value)

    def add_multiple(self, values: typing.Iterable):
        """Add multiple values from this node"""
        if not isinstance(values, typing.Iterable):
            raise TypeError('Method add_multiple accepts iterable data only for input.')

        for _value in set(values):
            self.add(_value)


def make_binary_search_tree(
    sorter: typing.Type[BaseSorter],
    values: list,
) -> BinarySearchTreeNode:
    """Build a BinarySearchTree instance from given values arguments"""
    root_node = BinarySearchTreeNode(sorter=sorter, node_value=values[0])
    root_node.add_multiple(values[1:])
    return root_node


integer_bst = make_binary_search_tree(sorter=IntegerSorter, values=[12])
integer_bst.add(4)
integer_bst.add(9)
integer_bst.add_multiple([5, 6, 7, 7])
