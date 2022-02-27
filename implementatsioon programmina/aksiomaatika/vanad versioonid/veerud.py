import copy
from inspect import getargspec
from sympy.logic import simplify_logic
from sympy.abc import symbols


def truthtable (n):
    if n < 1:
        yield []
        return
    subtable=truthtable(n-1)
    for row in subtable:
        for v in [False,True]:
            yield row+[v]
class Hulk():# võiks olla alamklass klassile Class from sympy.categories.baseclasses import Class#On mähisklass klassile set
    def __init__(self):
        self.elemendid=set()
    def __contains__(self, item):
        return item in self.elemendid
class Seos():#panna see laiendama klassi sympy class Seos(sympy):
    """
        Selle klassi eesmärk on panna hulkade vaheline seos kirja arvutile loetaval kujul. Alghulkadele vastava tähenduse valimisel võib seoset kasutada ka näiteks naturaalarvude,reaalarvude ja aritmeetiliste tehete defineerimiseks.
    """
    def __init__(self,p=None,almoisted=None):
        self.K=0#ajutine
        if type(p)==int:
            self.sisu_dnf_POS=p#disjunctive normal formi lõppveerg# DNF(disjunctive normal form)is paljude algmõistetega seose kirjeldamine võtab palju mälu. teha võimalus ka CNF(conjunctive normal form)is või NNF(Negation normal form)is kiseost salvestada.
        elif callable(p):
            self.argumendid=getargspec(p)[0]#funktsiooni argumentide nimetused
            #print(self.argumendid)
            self.N=p.__code__.co_argcount#N on algmoistete arv.
            if almoisted is not None and len(almoisted)!=self.N:
                quit("algmosteid ja algmoistete kirjeldusi pole sama palju.")
            print(self.get_veerud())
            v=[]
            for i in range(0, self.N):
                v.append(Hulk())
            self.sisu_dnf_POS=[]
            L=2**(self.N**2)-1
            self.sisu2=0
            for L in range(2**(self.N**2)-1,-1,-1):
                v2=copy.deepcopy(v)
                for i in range(0, self.N):
                    for j in range(0, self.N):
                        if ~L>>(self.N**2-i*self.N-j-1)&1:
                            v2[j].elemendid.add(v2[i])#ilma deepcopy'ta muudaks ka v'd, kuigi peab ainult v2 muutma.
                self.sisu_dnf_POS.append(p(*v2))
                if p(*v2):
                    self.sisu2= self.sisu2+2**L
                L-=1
    def __str__(self):
        print("hakkab sympyks teisendama")
        return str(self.get_sympy())
    def get_seos_ridadena(self):
        read=""
        i=0
        #veerud=self.get_veerud()
        for rea_booleanid in truthtable(len(self.get_veerud())):
            rida=""
            if self.sisu_dnf_POS[i]:#kui see rida on seosega kooskõlas.
                for o in range(0,len(rea_booleanid)):
                    if not rea_booleanid[o]:
                        rida+="¬"
                    rida+=("("+str(self.get_veerud()[o])+")∧")
                read+=rida[:-1]+"∨ "
            i=i+1
        return read[:-3]
    def get_veerud(self):
        veerud=[]
        for i in range(0, self.N):
            for j in range(0, self.N):
                veerud.append(self.argumendid[i]+"∈"+self.argumendid[j])
        return veerud
    def get_read(self):
        read=[]
        for rea_booleanid in truthtable(len(self.get_veerud())):
            rida=""
            for o in range(0, len(rea_booleanid)):
                if not rea_booleanid[o]:
                    rida+="¬"
                rida+=("("+str(self.get_veerud()[o])+")∧")
            read.append(rida)
        if self.K==0:
            return read
        elif self.K==1:

            return read
        return None
    def get_sympy(self):#tagastab tulemuse Sympy formaadis.
        veerud_sympy_formaadis=symbols(self.get_veerud())
        i=0#näitab, et mitmenda reaga on tegemist
        seos_sympy_formaadis=False
        for rea_booleanid in truthtable(len(self.get_veerud())):
            rida=True
            if self.sisu_dnf_POS[i]:#kui see rida on seosega kooskõlas.
                for o in range(0,len(rea_booleanid)):
                    if rea_booleanid[o]:
                        rida=rida&veerud_sympy_formaadis[o]
                    else:
                        rida=rida&~veerud_sympy_formaadis[o]
                seos_sympy_formaadis=seos_sympy_formaadis|rida#|=
            i=i+1
        print("seos valmis, kuid lihtsustamata")
        return simplify_logic(seos_sympy_formaadis)#tundub valesti lihtsustavat
    def get_K(self):
        pass
    def __and__(self,other):
        if not len(self.sisu_dnf_POS)==len(other.sisu):#self.K==other.K and self.N==other.N
            quit("erinev arg algmõisteid või kvantoreid")
        uus_sisu=[]
        for i in range(0, len(self.sisu_dnf_POS)):
            uus_sisu.append(self.sisu_dnf_POS[i] and other.sisu[i])
        return Seos(uus_sisu)
    def __or__(self,other):
        if not len(self.sisu_dnf_POS)==len(other.sisu):#self.K==other.K and self.N==other.N
            quit("erinev arg algmõisteid või kvantoreid")
        uus_sisu=[]
        for i in range(0, len(self.sisu_dnf_POS)):
            uus_sisu.append(self.sisu_dnf_POS[i] or other.sisu[i])
        return Seos(uus_sisu)
    def __xor__(self,other):
        if not len(self.sisu_dnf_POS)==len(other.sisu):#self.K==other.K and self.N==other.N
            quit("erinev arg algmõisteid või kvantoreid")
        uus_sisu=[]
        for i in range(0, len(self.sisu_dnf_POS)):
            uus_sisu.append(self.sisu_dnf_POS[i] != other.sisu[i])
        return Seos(uus_sisu)
def any(x_n,seos):#see on universaalsus kvantor.
    return symbols("∀x("+str(seos).strip(" ")+")")

def exists(x_n,seos):
    return lambda: not any(x_n,lambda: not seos)

#N=input("algmoisteid:")
#K=input("kvantoreid:")

def hulkade_funktsioon1(a, b, c, d):
    return (a in b and b in a) or (c in d and c in a)
def hulkade_funktsioon2(a,b):
    return (a in b and b in b)
def hulkade_funktsioon3(a):
    return (a in a)
def hulkade_funktsioon4(a,b,c):
    return (not a in a) and (b in a or c in a)
def kvantoriga_funktsioon(a,b):
    return (a in a) and any(0,lambda:x in a)

#seos1=Seos(hulkade_funktsioon2)
#seos2=Seos(hulkade_funktsioon4)
#print(seos2)

seos=Seos(hulkade_funktsioon3)
print(seos)