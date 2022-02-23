import copy#,sys
#sys.setrecursionlimit(5000)
def truthtable (n):
    if n < 1:
        yield []
        return
    subtable=truthtable(n-1)
    for row in subtable:
        for v in [0,1]:
            yield row+[v]
class Seos():
    def __init__(self,p):
        self.n=p.__code__.co_argcount
        self.kuva_veerud()
        v=[]
        for i in range(0,self.n):
            v.append([])
        self.t=[]
        for k in truthtable(self.n**2):
            v2=copy.deepcopy(v)
            for i in range(0,self.n):
                for j in range(0,self.n):
                    if k[i*self.n+j]:
                        v2[j].append(v2[i])#ilma deepcopy'ta muudaks ka v'd, kuigi peab ainult v2 muutma.
            print(*v2,k)
            self.t.append(p(*v2))
    def kuva_veerud(self):
        veerud=[]
        for i in range(0,self.n):
            for j in range(0,self.n):
                veerud.append(str(i)+" in "+str(j))
        print(veerud)



#N=input("algmoisteid:")
#K=input("kvantoreid:")

def hulkad_funktsioon(a, b, c, d):
    return (a in b and b in a) or (c in d and c in a)
seos=Seos(hulkad_funktsioon)


#a=[]
#b=[]
#a.append(b)
#b.append(a)
#print(a,b)