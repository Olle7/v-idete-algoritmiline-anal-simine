from sympy.logic import simplify_logic
from sympy.abc import symbols
import inspect
import sympy
#from sympy import Or,And
from sympy.logic.boolalg import to_dnf,to_cnf,to_nnf, BooleanFunction, Boolean,to_int_repr,term_to_integer
#from sympy import BooleanFunction
from sympy.categories.baseclasses import Class
#print(BooleanFunction)
a=symbols("a∈a")
b=symbols("a∈b")
c=symbols("b∈a")
d=symbols("b∈b")
#A=Class()
#print(A)
soos=(a&b&~c|d)&c
soos=to_nnf(soos)
print(term_to_integer(soos))
#soos=to_int_repr([to_cnf(soos)],[a,b,c,d])
print(soos,";",type(soos))
#soos=to_dnf(soos,simplify=True)
#print(soos,type(simplify_logic(soos)))
#print(inspect.getfile(soos.__class__))
#~x & ~y