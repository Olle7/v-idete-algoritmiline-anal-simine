from z3 import *

S = DeclareSort('S')
A=Function('A',S,BoolSort())
x1=Const("x1",S)
solve(And(Exists([x1],A(x1)),Not(Exists([x1],A(x1)))))#z3 annab õige tulemuse. ÜV

B=Function('B',S,BoolSort())
solve(And(Exists([x1],A(x1)),Not(Exists([x1],And(A(x1),B(x1))))))#z3 annab VIST õige tulemuse. mitte ÜV

solve(And(Exists([x1],And(A(x1),B(x1))),Not(Exists([x1],A(x1)))))#z3 annab õige tulemuse. ÜV

A2=Function('f', S, S,BoolSort())
x2=Const("x2",S)
x3=Const("x3",S)
solve(And(Exists([x1],Exists([x2],And(A2(x1,x2),Exists([x3],And(A2(x2,x3),A2(x2,x2)))))),Not(Exists([x1],Exists([x2],Exists([x3],And(A2(x2,x1),A2(x1,x3),A2(x1,x1))))))))#z3 nnab õige tulemuse. ÜV

on_mari=Function('on_mari',S,BoolSort())
M=Function('M',S,S,BoolSort())
solve(Or(And(Exists([x1],And(on_mari(x1),Not(Exists([x2],And(M(x1, x2),Exists([x3],And(M(x1, x3),Not(M(x2,x3)),M(x3, x1))),Exists([x3],And(M(x1, x3),M(x2, x3))),Not(Exists([x3],And(M(x2, x3),M(x3, x3))))))))),
Exists([x1],And(Exists([x2],And(
      on_mari(x2),
      M(x2,x1),
      Exists([x3],And(M(x1,x3),M(x2,x3))),
      Exists([x3],And(M(x2,x3),M(x3,x2),Not(M(x1,x3)))))),
Not(Exists([x2],And(
      M(x2,x1),
      M(x2,x2))))))),
Exists([x1],And(M(x1,x1),Not(Exists([x2],And(M(x1,x2),M(x2,x2),M(x2,x1))))))))#z3 annab VIST õige tulemuse. mitte ÜV

B2=Function('B', S, S,BoolSort())
C2=Function('C', S, S,BoolSort())
solve(And(
      Not(Exists([x1],And(Exists([x2],And(Or(B2(x2,x2),C2(x2,x2)),A2(x2,x2),Not(A2(x2,x1)))),Exists([x2],Or(B2(x2,x1),C2(x2,x1)))))),
      Exists([x1],And(A2(x1,x1),Or(B2(x1,x1),C2(x1,x1)))),
      Not(Exists([x1],Or(And(A2(x1,x1),Not(Exists([x2],And(Not(A2(x1,x2)),Exists([x3],Or(B2(x3,x2),C2(x3,x2))))))),Not(A2(x1,x1)))))
))

#solve(Exists([x1],And(A(x1 , x1 ),Exists([x2],A(x2 , x2 )∧A(x2 , x1 )∧A(x1 , x2 )),
#Exists([x2],Not(A(x2 , x2 ))∧Not(A(x1 , x2 ))∧A(x2 , x1 )∧Not(Exists([x3],Not(A(x3 , x3 ))∧Not(A(x3 , x2 ))∧A(x3 , x1 )∧A(x2 , x3 )∧A(x1 , x3 )))))∧Not(Exists([x1],Exists([x2],Exists([x3],¬A(x1 , x1 )∧
#Not(A(x1 , x2 ))∧Not(A(x2 , x1 ))∧Not(A(x2 , x2 ))∧Not(A(x3 , x1 ))∧Not(A(x3 , x2 ))∧Not(A(x3 , x3 ))∧Not(A(x1 , x3 ))∧Not(A(x2 , x3 ))))∨A(x1 , x1 )∧
#Exists([x2],A(x2 , x2 ) ∧ Not(A(x2 , x1 )) ∧ A(x1 , x2 )&¬Not(Exists([x3],Not(A(x3 , x3 )) ∧ A(x3 , x2 )¬∧ A(x3 , x1 ) ∧ A(x2 , x3 ) ∧ A(x1 , x3 )))))))