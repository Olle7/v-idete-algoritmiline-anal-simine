from poolikud.seos_Oga import *
from poolikud.seos2 import *


A=Predikaat("A")

#print("test1:",mitte_ÜV(U(U(U(U(A(0)|A(1)|A(2)))))))

#print("test2:",mitte_ÜV(U(~U(U(A(0)&A(1)|A(2))))))

#print("test3:",mitte_ÜV(~U(A(0))))
#print("test4:",mitte_ÜV(~U(A(0)&A(1))))
print("test5:",mitte_ÜV(U(A(10)&A(11))&~U(A(0)&A(1))&~U(A(2))|U(A(9))))