from sympy import Symbol, to_dnf
r1,r2,r3,r4=Symbol("r1"),Symbol("r2"),Symbol("r3"),Symbol("r4")
boolean_väide=r1|r2|(r3&~r1)
print(to_dnf(boolean_väide,True))

#E(H1(x)|H2(x)|(H3(x)&~H1(x)))
#E(H1(x)) | E(H2(x)) | E(H3(x)&~H1(x))
#E(H2(x)) | E(H3(x)&~H1(x))|E(H1(x))
#E(H2(x))|E(H3(x))|E(H1(x))