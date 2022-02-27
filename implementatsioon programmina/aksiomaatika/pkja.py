from math import log
def pkj_a(arvud):
    arvud.reverse()
    V=0
    a=0
    for arv in arvud:
        arv+=2
        bitte_arvus=int(log(arv,2))
        #print(bitte_arvus,"bitti arvule",arv,"ehk",bin(arv))
        b_b=int(log(bitte_arvus,2))
        s=b_b*"0"+bin(bitte_arvus)[2:]+bin(arv)[3:]
        v=int(s,2)
        print(v,a)
        V+=v*2**a
        print(arv,";",s,";",v)
        #pkt=(2**b_b-1)*2**(b_b*bitte_arvus)
        #pkt+=bitte_arvus
        #print(bin(pkt))
        print("V=",bin(V))
        a += len(s)
        input()


def pkj_d(data):
   pass

if __name__=="__main__":
    print(pkj_a([2,4,100,500,2,0]))