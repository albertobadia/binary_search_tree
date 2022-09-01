import functools
import typing

from sorters import BaseSorter
from errors import EqualValuesException, InvalidTypeException, RootNodeDeleteException


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

    _left_node: "BinarySearchTreeNode" = None
    _right_node: "BinarySearchTreeNode" = None

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
        return self.depth, [
            i.node_value for i in self.leaf_nodes if i.level == self.depth
        ]

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

    def get_ordered_values(self, reverse: bool = False) -> list[typing.Any]:
        """Get all values in a given order"""
        result = []

        side_order = ["_left_node", "_right_node"]
        if reverse:
            side_order.reverse()

        first_side_node = getattr(self, side_order[0], None)
        if first_side_node is not None:
            result += first_side_node.get_ordered_values(reverse=reverse)

        result.append(self.node_value)

        second_side_node = getattr(self, side_order[1], None)
        if second_side_node is not None:
            result += second_side_node.get_ordered_values(reverse=reverse)

        return result

    def cache_clear(self):
        """
        Multiple properties on this class has cache (memoization), so we have to
        clear / invalidate cache to force tree re-calculate cached keys in order to show new info.
        """
        for attr in dir(type(self)):  # <- for every node attribute
            if isinstance(
                getattr(type(self), attr), functools.cached_property
            ):  # <- check if is a cached_property
                vars(self).pop(attr, None)  # <- Then delete the actual value

    def add(self, value: typing.Any):
        """
        Add single value, it will be validated by sorter adapter at compare step.
        """
        try:
            # Get the side destination for this value
            side = (
                "_left_node"
                if self.sorter.is_lower_than(value, self.node_value)
                else "_right_node"
            )
            side_node = getattr(self, side, None)

            if side_node is not None:
                side_node.add(
                    value
                )  # <- We already have a node on the side, so we call it's own add method
            else:
                # In case we dont have a node, we create one with new value
                created_node = BinarySearchTreeNode(
                    sorter=self.sorter,
                    node_value=value,
                    level=self.level + 1,
                )
                setattr(self, side, created_node)  # <- put the node in a side of parent

            self.cache_clear()

        except EqualValuesException:
            # We do nothing for now
            return

    def remove(self, value: typing.Any):
        """
        Delete the node that match a certain value
        """
        try:
            if (
                value == self.node_value
            ):  # <- The root node is the only one we cannot delete
                if self.is_root:
                    raise RootNodeDeleteException("Cannot remove root node.")

            side = (
                "_left_node"
                if self.sorter.is_lower_than(value, self.node_value)
                else "_right_node"
            )
            side_node = getattr(self, side, None)

            if side_node is not None:
                if side_node.node_value == value:
                    setattr(self, side, None)
                    return True

                side_node.remove(value)
            return False

        finally:
            self.cache_clear()

    def add_multiple(self, values: typing.Iterable):
        """
        Add multiple values from this node
        """
        if not isinstance(values, typing.Iterable):
            raise InvalidTypeException(
                "Method add_multiple accepts iterable data only for input."
            )

        for _value in values:
            self.add(_value)
