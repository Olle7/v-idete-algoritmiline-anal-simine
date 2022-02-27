from sage.crypto.boolean_function import BooleanFunction

b = list([1, 0, 0, 1])  # add your list here
B = BooleanFunction(b)
print
B.algebraic_normal_form()