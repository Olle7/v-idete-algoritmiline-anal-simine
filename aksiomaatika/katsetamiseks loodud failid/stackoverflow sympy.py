from sympy.core.symbol import Symbol
from sympy.logic.boolalg import Equivalent
from sympy import simplify_logic
a=Symbol("a")
b=Symbol("b")
c=Symbol("c")
d=Symbol("d")
e=Symbol("e")

expr=simplify_logic(a&b>>c|a&d|~a&Equivalent(c,(d|a&e)|b))
print(simplify_logic(expr))
print("if a=True and d=False, then relation between a,c and e must be")#c|~b
eeldus=a&~d


print(simplify_logic(expr.subs(a,True)))