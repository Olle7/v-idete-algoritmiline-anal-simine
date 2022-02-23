from sympy.abc import symbols
from sympy import simplify_logic
t1,t2,t3,v1,v2,v3=symbols(["t1","t2","t3","v1","v2","v3"])
expr=t1>>v1&t2>>v2&t3>>v3
expr2=t1&v1|t2&v2|t3&v3
print(expr,expr2)
print(simplify_logic(expr),simplify_logic(expr2))
print(simplify_logic(expr)==simplify_logic(expr2))#False