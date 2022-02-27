from sympy import *
from sympy.abc import symbols

AinA,AinB,BinA,BinB=symbols(["A∈A","A∈B","B∈A","B∈B"])
print(type(AinA))

r0=simplify((~AinA|~AinB|~BinA)&(~AinB|~BinA|~BinB))
print(type(r0))
print(r0)

r1=(~AinA|~BinA|AinB)&(~BinB|~AinB|~BinA|BinB)
print(to_cnf(r1))