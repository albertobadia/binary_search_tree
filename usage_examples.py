from make_bst import make_binary_search_tree


integer_bst = make_binary_search_tree(values=[12])
integer_bst.add(4)
integer_bst.add(9)
integer_bst.add_multiple([5, 21, 6, 7, 7, 19])

char_bst = make_binary_search_tree(values=["a", "c", "z", "m", "y"])

# error_bst = make_binary_search_tree(values=['a', 1, 0.5, 'b'])

print(integer_bst.get_ordered_values(reverse=True))
integer_bst.remove(21)
integer_bst.remove(33)
