from sympy import *
from sympy.abc import symbols
v0,v1,v2,v3,v4,v5,v6,v7=symbols("v0,v1,v2,v3,v4,v5,v6,v7")
f2=simplify(v0>>False&v1>>True& v2>>False&v3>>True& v4>>False&v5>>True& v6>>False&v7>>True)
f1=simplify(v0>>f2&v1>>f2&v2>>f2&v3>>f2&v4>>f2&v5>>f2)
print("f2=",f2)
print(f1)

käsitsi_lihtsustatud_f1=simplify(~v0&~v2&~v4&((v1|v3|v5)>>~v6))
print(käsitsi_lihtsustatud_f1.equals(f1))