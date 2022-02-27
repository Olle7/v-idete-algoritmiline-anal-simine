from sympy.ntheory import factorint
def f(N):
    return 2**(N**2)*(2**(2**N)-1)**(2**(N+1))
def f1(N):
    return 2**(2**N)-1

i=0
while True:
    i+=1
    print(i)
#    print(factorint(f1(i)))

    if len(set(factorint(f1(i)).values()))!=1:
        print(i,"ühe algteguri aste ei ole 1")