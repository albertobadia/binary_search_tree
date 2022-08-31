import functools
import typing

from sorters import BaseSorter, IntegerSorter


class BinarySearchTreeNode:
    """
    This is a Binary search tree node, which has left and right child nodes of same class
    """
    def __init__(
        self,
        sorter: typing.Type[BaseSorter],
        node_value: typing.Any,
        level: int = 0,
    ):
        self.sorter = sorter
        self.node_value = node_value
        self.level = level

    _left_node = None
    _right_node = None

    @property
    def is_root(self) -> bool:
        """Check if is the root node"""
        return self.level == 0

    @functools.cached_property
    def leaf_nodes(self) -> list[typing.Any]:
        """
        Returns all leaf nodes recursively
        """
        if self._left_node is None and self._right_node is None:
            return [self]

        result = []
        if self._left_node is not None:
            result += self._left_node.leaf_nodes
        if self._right_node is not None:
            result += self._right_node.leaf_nodes
        return result

    @functools.cached_property
    def depth(self):
        """Returns the depth of whole tree, it can be asked from any node"""
        return max(set(i.level for i in self.leaf_nodes))

    @functools.cached_property
    def deepest_nodes(self) -> tuple[int, list]:
        """Returns a tuple with 2 items:
            int:            depth of whole tree
            [values...]     deepest nodes values
        """
        return self.depth, [i.node_value for i in self.leaf_nodes if i.level == self.depth]

    @functools.cached_property
    def min_value(self):
        """Get the lowest value of tree"""
        if self._left_node is not None:
            return self._left_node.min_value
        return self.node_value

    @functools.cached_property
    def max_value(self):
        """Get the higher value of tree"""
        if self._right_node is not None:
            return self._right_node.max_value
        return self.node_value

    def cache_clear(self):
        """
        Multiple properties on this class has cache (memoization) assigned to,
        so we have to clear / invalidate cache to force tree re-calculate cached keys.
        """
        for attr in dir(type(self)):
            if isinstance(getattr(type(self), attr), functools.cached_property):
                vars(self).pop(attr, None)

    def add(self, value):
        """Add single value"""

        try:
            if self.sorter.is_lower_than(value, self.node_value):
                destination_side = '_left_node'
            else:
                destination_side = '_right_node'

            side_node = getattr(self, destination_side, None)
            if side_node is not None:
                side_node.add(value)
            else:
                created_node = BinarySearchTreeNode(
                    sorter=self.sorter,
                    node_value=value,
                    level=self.level + 1,
                )
                setattr(self, destination_side, created_node)

            self.cache_clear()

        except ValueError:
            # We do nothing for now
            return

    def add_multiple(self, values: typing.Iterable):
        """Add multiple values from this node"""
        if not isinstance(values, typing.Iterable):
            raise TypeError('Method add_multiple accepts iterable data only for input.')

        for _value in set(values):
            self.add(_value)


def make_binary_search_tree(
    sorter: typing.Type[BaseSorter],
    values: list[typing.Any],
) -> BinarySearchTreeNode:
    """Build a BinarySearchTree instance from given values arguments"""
    root_node = BinarySearchTreeNode(sorter=sorter, node_value=values[0])
    root_node.add_multiple(values[1:])
    return root_node


integer_bst = make_binary_search_tree(sorter=IntegerSorter, values=[12])
integer_bst.add(4)
integer_bst.add(9)
integer_bst.add_multiple([5, 6, 7, 7, 19])

print(integer_bst)

pass
