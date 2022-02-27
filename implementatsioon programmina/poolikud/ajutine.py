<from sympy import Symbol, to_dnf, Or, And, Not,Nand,Nor,Xor
r1,r2,r3,r4=Symbol("r1"),Symbol("r2"),Symbol("r3"),Symbol("r4")
boolean_väide=Xor((Nor((~r1 | r2),(r1 & r3))),(r2 | r4))>
((\neq r1 \lor r2)NOR(r1 \land r3)) XOR (r2 \lor r4)

print(to_dnf(boolean_väide,True))