import functools
import typing

from sorters import BaseSorter
from errors import EqualValuesException, InvalidTypeException, RootNodeDeleteException
from cache_manager import CacheManager


class BinarySearchTreeNode(CacheManager):
    """
    The node is the core of the binary search tree, because the tree actually is
    a network of nodes with none, one, or two children.
    When we add a new value, we actually call root node <add> method, it places
    the value on left or right side depending on is lower or higher than parent.
    Consider the following tree:

                43         # root node
               /  \
             21    89      # child nodes
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
        return self.level == 0

    @functools.cached_property
    def leaf_nodes(self) -> list[typing.Any]:
        """
        Any node that does not have any child is considered a leaf node.
        Example:
                        86
                       /  \
                     50    105  <- leaf
                    /  \
       leaf ->    21    65
                        /
                       60  <- leaf
        """
        if self._left_node is None and self._right_node is None:
            return [self]  # <- no children so is a leaf node, we return a list to merge recursively

        result = []
        if self._left_node is not None:
            result += self._left_node.leaf_nodes
        if self._right_node is not None:
            result += self._right_node.leaf_nodes
        return result

    @functools.cached_property
    def depth(self):
        """
        The depth is the highest level that any node has, or we can also say,
        that is the max number of jumps that any node make to bring into its place.
        Example:                    77          <- level 0, root
                                   /  \
                                 55    94       <- level 1
                                /
                               13               <- level 2, so depth = 2

        """
        return max(set(i.level for i in self.leaf_nodes))

    @functools.cached_property
    def deepest_nodes(self) -> tuple[int, list]:
        """
        Deepest nodes are nodes that are at the same level of tree depth (see depth property),
        Example:          68  result = (1, [37, 92])
                         /  \
                       37    91
        Returns a tuple with 2 items:
        int:            depth of whole tree
        [values...]     deepest nodes values
        """
        return self.depth, [
            i.node_value for i in self.leaf_nodes if i.level == self.depth
        ]

    @functools.cached_property
    def min_value(self):
        """Get the lowest value of whole tree"""
        if self._left_node is not None:
            return self._left_node.min_value
        return self.node_value

    @functools.cached_property
    def max_value(self):
        """Get the higher value of whole tree"""
        if self._right_node is not None:
            return self._right_node.max_value
        return self.node_value

    def get_ordered_values(self, reverse: bool = False) -> list[typing.Any]:
        """
        Get a list of all tree nodes value by ordering using internal sorter.
        For example:

        tree with values = [5, 3, 7, 2, 9, 1] returns [1, 2, 3, 5, 7, 9] (or reverse)
        """
        result = []

        sides_order = ["_left_node", "_right_node"]
        if reverse:
            sides_order.reverse()

        first_side_node = getattr(self, sides_order[0], None)
        if first_side_node is not None:
            result += first_side_node.get_ordered_values(reverse=reverse)

        result.append(self.node_value)

        second_side_node = getattr(self, sides_order[1], None)
        if second_side_node is not None:
            result += second_side_node.get_ordered_values(reverse=reverse)

        return result

    def add(
            self,
            value: typing.Any,
            bypass_cache_clear: bool = False,  # <- when we use <add_multiple> calls at the end only.
    ):
        """
        Add a value to tree, we should do it from root only, value placement and validation
        will be resolved by self sorter.
        When we add a new value, the root check if is lower or higher using sorter,
        then check if there's already a child node, if is, call the child add method
        and the rest is the same.
        Example:               50           <- we add 59, is higher so put to right, there
                              /   \n           is already a node, so we call <add> from it.
                            25     76       <- is lower, we put on left and there is no node.
                                  /
                                59          <- ends here
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
                )  # <- We already have a node on the side, so we call its own add method
            else:
                # In case we don't have a node, we create one with new value
                created_node = BinarySearchTreeNode(
                    sorter=self.sorter,
                    node_value=value,
                    level=self.level + 1,
                )
                setattr(self, side, created_node)  # <- put the node in a side of parent

        except EqualValuesException:
            # We do nothing for now
            return
        finally:
            self.clear_cached_properties()

    def remove(self, value: typing.Any):
        """
        Delete the node that match a certain value and its children,
        we find the node using the tree structure. We know the path
        to follow by checking if is lower or higher.
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
            self.clear_cached_properties()

    def add_multiple(self, values: typing.Iterable):
        """
        Add multiple values from this node
        """
        if not isinstance(values, typing.Iterable):
            raise InvalidTypeException(
                "Method add_multiple accepts iterable data only for input."
            )

        for _value in values:
            self.add(_value, bypass_cache_clear=True)
        self.clear_cached_properties()
