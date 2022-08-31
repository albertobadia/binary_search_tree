from errors import MultipleDataTypesException
from make_bst import make_binary_search_tree
from sorters import FloatSorter, CharSorter, IntegerSorter

integer_bst = make_binary_search_tree(values=[12])  # Make a BST with one value only
# Add individual values
integer_bst.add(4)
integer_bst.add(9)
# Add multiple values
integer_bst.add_multiple([5, 21, 6, 7, 7, 19])
assert integer_bst.sorter == IntegerSorter  # <- validate sorter

assert integer_bst.get_ordered_values() == [4, 5, 6, 7, 9, 12, 19, 21]
integer_bst.remove(21)
integer_bst.remove(33)

#########################################################################

# Make a Char based BST
char_bst = make_binary_search_tree(values=["a", "c", "z", "m", "y"])
assert char_bst.sorter == CharSorter

#########################################################################

# Make a float based BST
float_bst = make_binary_search_tree(values=[0.1, 0.2, 4.3])
assert float_bst.sorter == FloatSorter

#########################################################################

try:
    error_bst = make_binary_search_tree(values=["a", 1, 0.5, "b"])
except MultipleDataTypesException:
    # This is an expected error
    pass
