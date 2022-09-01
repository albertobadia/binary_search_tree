import unittest

from make_bst import make_binary_search_tree


class BinarySearchTreeNode(unittest.TestCase):
    """
    The node is the core of business logic, a binary search tree is really a root node with child/ren.
    Here we test the properties and method for these nodes, that as we said, are actually for the entire tree.
    Not bugs here, dev god please...
    """

    def test_is_root_true_no_children(self):
        """
        The only value should be result in a node with: is_root = True, level = 0 and no children
        """
        int_bst = make_binary_search_tree(values=[1])
        self.assertEqual(int_bst.node_value, 1)
        self.assertTrue(int_bst.is_root)
        self.assertEqual(int_bst.level, 0)
        self.assertIsNone(int_bst._left_node)
        self.assertIsNone(int_bst._right_node)

    def test_is_root_true_with_children(self):
        """
        Create binary search tree with multiple values, the first one should
        result in a node with: is_root = True, level = 0, _left_node and _right_node children
        """
        char_bst = make_binary_search_tree(values=["d", "m", "a"])
        self.assertEqual(char_bst.node_value, "d")
        self.assertTrue(char_bst.is_root)
        self.assertEqual(char_bst.level, 0)
        self.assertEqual(char_bst._left_node.node_value, "a")
        self.assertEqual(char_bst._right_node.node_value, "m")

    def test_nested_placement(self):
        """
        When we decide the side to put a new node, if we found a existing node on that side
        we left the work of decide how to handle this to it.
        """
        float_bst = make_binary_search_tree(values=[10.5, 23.4, 5.8, 20.5])
        self.assertEqual(float_bst.node_value, 10.5)
        self.assertEqual(float_bst._right_node._left_node.node_value, 20.5)

    def test_leaf_nodes(self):
        """
        Leaf nodes are nodes that does not have any child, the end of the tree.
        """
        int_bst = make_binary_search_tree(values=[50, 100, 25, 75, 12])
        self.assertEqual(
            [i.node_value for i in int_bst.leaf_nodes],
            [12, 75],
        )

    def test_depth(self):
        """
        The depth of tree is number of level it has consider the following tree:

                        3          level 0
                      /   \
                    1     10       level 1    ( 2 depth tree)
                         /
                        5          level 2
        """
        float_bst = make_binary_search_tree(values=[50.64, 100.32, 25.65, 13.4, 7.5])
        self.assertEqual(float_bst.depth, 3)

    def test_deepest_nodes(self):
        """
        This method should return:
        tuple of (depth of tree, list[node/s that are at lowest highest level...]).
        Check the following tree:

                        "M"
                       /   \
                     "D"   "Y"
                    /
                  "C"                <- deepest_nodes = (2, ["C"]) : tuple
        """
        char_bst = make_binary_search_tree(values=["M", "D", "Y", "C"])
        self.assertEqual(char_bst.deepest_nodes, (2, ["C"]))

    def test_min_value(self):
        """
        This value should the lowest one in the tree (or down bellow the node where it was read).
        """
        int_bst = make_binary_search_tree(values=[5, 7, 1, 7, 46, 12, 78, 33])
        self.assertEqual(int_bst.min_value, 1)

    def test_max_value(self):
        """
        This value should the highest one in the tree (or down bellow the node where it was read).
        """
        int_bst = make_binary_search_tree(values=[5, 7, 1, 7, 46, 12, 78, 33])
        self.assertEqual(int_bst.max_value, 78)

    def test_ordered_values(self):
        """
        This method should return an ordered list of all values on tree.
        """
        int_bst = make_binary_search_tree(values=[5, 7, 1, 7, 46, 12, 78, 33])
        self.assertEqual(int_bst.get_ordered_values(), [1, 5, 7, 12, 33, 46, 78])

    def test_ordered_values_reverse(self):
        """
        This method should return an ordered list of all values on tree
        """
        int_bst = make_binary_search_tree(values=[5, 7, 1, 7, 46, 12, 78, 33])
        self.assertEqual(
            int_bst.get_ordered_values(reverse=True), [78, 46, 33, 12, 7, 5, 1]
        )

    def test_add(self):
        """
        Test add method by checking min value
        """
        char_bst = make_binary_search_tree(values=["z", "x", "f"])
        char_bst.add("a")
        self.assertEqual(char_bst.min_value, "a")

    def test_remove(self):
        """
        Test add method by checking max value
        """
        char_bst = make_binary_search_tree(values=["a", "x", "f", "z"])
        self.assertEqual(char_bst.max_value, "z")
        char_bst.remove("z")
        self.assertEqual(char_bst.max_value, "x")

    def test_add_multiple(self):
        """
        Test add_multiple by checking ordered_values
        """
        float_bst = make_binary_search_tree(values=[1.1, 2.2, 3.3, 4.4])
        self.assertEqual(float_bst.get_ordered_values(), [1.1, 2.2, 3.3, 4.4])
        float_bst.add_multiple([5.5, 6.6, 7.7, 8.8, 9.9])
        self.assertEqual(
            float_bst.get_ordered_values(),
            [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9],
        )

    def test_challenge_example_1(self):
        int_bst = make_binary_search_tree(values=[12, 11, 90, 82, 7, 9])
        self.assertEqual(int_bst.deepest_nodes, (3, [9]))

    def test_challenge_example_2(self):
        int_bst = make_binary_search_tree(values=[26, 82, 16, 92, 33])
        self.assertEqual(int_bst.deepest_nodes, (2, [33, 92]))
