# Binary seach tree example

![Alt text](bst_diagram.jpg?raw=true "Title")

## Usage examples:

``` Python
from errors import MultipleDataTypesException
from make_bst import make_binary_search_tree
from sorters import FloatSorter, CharSorter, IntegerSorter

integer_bst = make_binary_search_tree(values=[12, 11, 90, 82, 7, 9])
assert integer_bst.sorter == IntegerSorter  # <- validate sorter
assert integer_bst.get_ordered_values() == [7, 9, 11, 12, 82, 90]
assert integer_bst.deepest_nodes == (3, [9])

#########################################################################

# Make a Char based BST
char_bst = make_binary_search_tree(values=["a", "c", "z", "m", "y"])
assert char_bst.get_ordered_values() == ["a", "c", "m", "y", "z"]
assert char_bst.sorter == CharSorter

#########################################################################

# Make a float based BST
float_bst = make_binary_search_tree(
    values=[75.44, 55.11, 0.1, 66.33, 0.2, 100.1, 4.3, 45.4, 50.56]
)
assert float_bst.sorter == FloatSorter
assert float_bst.get_ordered_values() == [
    0.1,
    0.2,
    4.3,
    45.4,
    50.56,
    55.11,
    66.33,
    75.44,
    100.1,
]

#########################################################################

try:
    error_bst = make_binary_search_tree(values=["a", 1, 0.5, "b"])
except MultipleDataTypesException:
    # This is an expected error
    pass
```
