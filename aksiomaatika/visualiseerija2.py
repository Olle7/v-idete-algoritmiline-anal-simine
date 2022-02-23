class Predikaat():
    def __init__(self,nimi,argumente,argumentide_järjekord_oluline=True):
        self.nimi=nimi
        self.argumente=argumente
        self.argumentide_järjekord_oluline=argumentide_järjekord_oluline

class Plato():
    def __init__(self,tase,number,predikaadid,K):
        self.K=K
        self.tase=tase
        self.number=number
        self.predikaadid=predikaadid
    def __str__(self):
        #print(veerge(1,self.predikaadid,self.K))
        return (preds(predikaadid,self.tase))

def preds(predikaadid,tase):
    if tase==-1 or tase==0:#kui plato on LV(lõppveerg) või LR(lõpprida).
        return ""
    s=""
    for predikaat in predikaadid:
        args = []
        for i in range(predikaat.argumente):
            args.append(1)
        while True:
            if tase in args:
                s+=predikaat.nimi+"("
                for argumendi_indeks in range(len(args)-1):
                    s+="x_"+str(args[argumendi_indeks])+","
                s += "x_" + str(args[len(args)-1])
                s+=") AND "
            for i in range(predikaat.argumente):
                if args[-i-1]==tase:
                    args[-i - 1]=1
                else:
                    args[-i-1]+=1
                    break
            else:
                break
    return s


def H_bitte(tase,predikaadid):#et mitu bitti on platonumbri alguss seosefunktsioonide väärtuste näitamiseks.
    H=0
    if tase==-1 or tase==0:
        return 0
    for predikaat in predikaadid:
        H+=tase**(predikaat.argumente)-(tase-1)**(predikaat.argumente)#vaja lahutada nende võimalust bitid, mis ei sisalda kõrgeimat kvanteeritavat.
    return H
def veerge(tase,predikaadid,K):
    veerge2=0
    for i in range(K,tase,-1):
        veerge2=2**(veerge2*+H_bitte(i,predikaadid))
    return veerge2



predikaadid=[Predikaat("A",3,False)]
#print(Plato(2,55,predikaadid,2))

print(H_bitte(2,predikaadid))