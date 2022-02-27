import copy
from inspect import getargspec
from sympy.logic import simplify_logic
from sympy.abc import symbols
import sympy
from Seose_parssija import Seose_parssija

def truthtable (n):#asendada see igal pool üle täisarvude itereerimisega.
    if n < 1:
        yield []
        return
    subtable=truthtable(n-1)
    for row in subtable:
        for v in [False,True]:
            yield row+[v]
class Hulk():
    def __init__(self):
        self.elemendid=set()
    def __contains__(self, item):
        return item in self.elemendid
class Seos():#panna see laiendama klassi sympy class Seos(sympy):
    """
        Selle klassi eesmärk on panna hulkade vaheline seos kirja arvutile loetaval kujul. Alghulkadele vastava tähenduse valimisel võib seoset kasutada ka näiteks naturaalarvude,reaalarvude ja aritmeetiliste tehete defineerimiseks.
    """
    def __init__(self, seos_muus_formaadis, K=None, N=None,alghulgad=None,alghulkade_kirjeldused=None):
        if type(seos_muus_formaadis)==int:
            self.K=K
            self.N=N
            if alghulgad:
                self.alghulgad=alghulgad
            else:
                self.alghulgad=[]
                for i in range(0,N):
                    self.alghulgad.append("H"+str(i))
            self.ns=seos_muus_formaadis
        elif type(seos_muus_formaadis)==str:#loeb seose mingist texti formaadist. Näiteks "∀x(x∈A)"
            seos_muus_formaadis=Seose_parssija(seos_muus_formaadis)
            exit("pole valmis")
            self.ns=0
            uue_indekseeringuga_rea_nr=0
            for rea_nr in range(0,2**(self.N**2+2**(self.K*(1+self.N*2)))):
                if teeb_kõigi_hulkade_kohta_väiteid(rea_nr) or alghulkade_veerud_on_vastuolus_kvantori_veergudega(rea_nr) or on_teistsuguse_reaga_kirjeldatav(rea_nr):
                    continue
                uue_indekseeringuga_rea_nr+=1
                if False:#kui on kooskõlas seosega
                    self.ns+=2**uue_indekseeringuga_rea_nr
        elif callable(seos_muus_formaadis):#kui tegu on pythoni funktsiooniga hulkade vahel.#Raske teostada, sest mõuab palju itereerimist.
            print(seos_muus_formaadis)
            self.K=0# ajutine
            self.alghulgad=getargspec(seos_muus_formaadis)[0]#funktsiooni argumentide nimetused
            if alghulgad and self.alghulgad!=alghulgad:
                quit("funktsioonil, millest seos tehakse on teistsugused argumendid.")
            self.N=seos_muus_formaadis.__code__.co_argcount#N on algmoistete arv.
            if alghulkade_kirjeldused is not None and len(alghulkade_kirjeldused)!=self.N:
                quit("algmosteid ja algmoistete kirjeldusi pole sama palju.")
            alghulgad=[]
            #iga universaalsuskvantor jaatab teatud veerud ja iga eksistentsiaalkvantor eitab teatud veerud.
            for i in range(0,self.N):
                alghulgad.append(Hulk())


            self.ns=0#sisu DNF formaadis. lisaks DNFile võiks see võimaldada salvestada seose mingis muus normaalvormis, nii ,et osade parameetrite dnf tulemuse ja ülejäänud parameetrid on muu normaalvormi elemendid.
            for rea_nr in range(2**self.N**2):
                v2=copy.deepcopy(alghulgad)
                for i in range(0, self.N):
                    for j in range(0,self.N):
                        if not not(rea_nr&(1<<(self.N**2-1-i*self.N-j))):
                            v2[j].elemendid.add(v2[i])#ilma deepcopy'ta muudaks ka v'd, kuigi peab ainult v2 muutma.
                if seos_muus_formaadis(*v2):#h_i in H_j
                    self.ns+= 2 ** rea_nr
        elif isinstance(seos_muus_formaadis,sympy.logic.boolalg.BooleanFunction):#tegu on sympy avaldisega, mille sisse on passiivseid kvantoreid pandud.#Rakse teostada, sest __contains__ tagastab ainult booleane.
            exit("pole valmis")
        #jätab alghulkade kuuluvuste vahelised seosed samaks, aga muudab need sympy symboliteks.
        #toob kvantorite seest alghulkade omavahelised kuuluvused välja
        #kvantorid muudab kvantoriveergude vahelisteks booleankombinatsioonideks(võibolla vaja hoopis booleanide vahelisi seoseid)
        #kvantoriveerud muudab sympy sümboliteks.
        #lõpuks laseb sympyl sympy sümbolite vahelise seose lihtsustada.

    def __str__(self):
        return str(self.get_sympy())
    def get_seos_ridadena(self):
        read=""
        i=0
        #veerud=self.get_veerud()
        for rea_booleanid in truthtable(len(self.get_veerud())):
            rida=""
            if self.sisu[i]:#kui see rida on seosega kooskõlas.
                for o in range(0,len(rea_booleanid)):
                    if not rea_booleanid[o]:
                        rida+="¬"
                    rida+=("("+str(self.get_veerud()[o])+")∧")
                read+=rida[:-1]+"∨ "
            i=i+1
        return read[:-3]
    def get_veerud(self):#VALE! SELLISTE VVEGUDEGA EI SAA KÕIKI SEOSEID KIRJELDADA
        """
        :return:DNF tabeli, mis seost kirjeldab veerud.
        """
        veerud=[]
        k_veerge=1
        for i in range(1,self.K+1):
            k_veerge*=2**(i**2-i+2*self.N+1)-1
        veerge_väiksemate_kde_korral=k_veerge
        for i in range(0,k_veerge):
            veerud.append("")
        for k in range(1,self.K+1):
            väikesed_veerud=[]#pole kindel, et kas see järjekord on parim.
            for k2 in range(1,k+1):
                väikesed_veerud.append("x"+str(k)+"∈x"+str(k2))
            for n in range(0,self.N):
                väikesed_veerud.append("x"+str(k)+"∈"+self.alghulgad[n])
            for k2 in range(1,k):
                väikesed_veerud.append("x"+str(k2)+"∈x"+str(k))
            for n in range(0,self.N):
                väikesed_veerud.append(self.alghulgad[n]+"∈"+"x"+str(k))
            print(väikesed_veerud)
            väikeseid_ridu_antud_k_korral=k*(k-1)+2*self.N+1
            veerge_väiksemate_kde_korral-=2**väikeseid_ridu_antud_k_korral#SIIN VIGA!
            #veerge_väiksemate_kde_korral=0
            #print(veerge_väiksemate_kde_korral)
            for veeru_nr in range(0,k_veerge):
                veerg="∀x"+str(k)+"("
                for väikese_veeru_nr in range(0,väikeseid_ridu_antud_k_korral):
                    if (not(veeru_nr&(1<<(väikeseid_ridu_antud_k_korral+veerge_väiksemate_kde_korral-väikese_veeru_nr-1)))):
                        veerg+=" ¬"
                    veerg+=väikesed_veerud[väikese_veeru_nr]+" ∧ "
                veerud[veeru_nr]+=veerg
        for i in range(0, k_veerge):
            veerud[i]+=self.K *")"
        for i in range(0, self.N):#lisab Q veerud(alghulkade omavahelist kuuluvust kirjeldavad veerud).
            for j in range(0, self.N):
                veerud.append(self.alghulgad[i] + "∈" + self.alghulgad[j])
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
    def get_rida(self,rea_nr):
        pass
    def get_veerg(self,veeru_nr):
        pass
    def get_sympy(self):#tagastab tulemuse Sympy formaadis.
        veerud_sympy_formaadis=symbols(self.get_veerud())
        seos_sympy_formaadis=False
        for rea_nr in range(2**(self.N**2)):
            if (self.ns>>rea_nr)&1:#kui see rida on seosega kooskõlas.
                rida=True
                for veeru_number in range(0,self.N**2):
                    if not(rea_nr&(1<<(self.N**2-1-veeru_number))):#kui rea boolean on False
                        rida&=~veerud_sympy_formaadis[veeru_number]
                    else:#kui rea boolean on True
                        rida&=veerud_sympy_formaadis[veeru_number]
                seos_sympy_formaadis|=rida#
        #print(seos_sympy_formaadis)
        return simplify_logic(seos_sympy_formaadis)#tundub valesti lihtsustavat
    def get_K(self):
        return self.K
    def __and__(self,other):
        if not self.K==other.K and self.alghulgad==other.alghulgad:
            exit("pole valmis")
            #quit("erinev arv algmõisteid või kvantoreid")
        return Seos(self.ns & other.sisu2, self.K, self.N, self.alghulgad)
    def __or__(self,other):
        #if not len(self.sisu)==len(other.sisu):#self.K==other.K and self.N==other.N
        #    quit("erinev arg algmõisteid või kvantoreid")
        return Seos(self.ns | other.sisu2, self.K, self.N, self.alghulgad)
    def __xor__(self,other):
        #if not len(self.sisu)==len(other.sisu):#self.K==other.K and self.N==other.N
        #    quit("erinev arg algmõisteid või kvantoreid")
        return Seos(self.ns ^ other.sisu2, self.K, self.N, self.alghulgad)
class passiivne_any():#see on universaalsus kvantor.
    def __init__(self,x_n,seos):
        self.seos=seos
        self.x_n=x_n#x_n näitab, et mistahes mitmenda argumendi väärtuse korral peaob seos kehtima.
class passiivne_exists():
    def __init__(self,x_n,seos):
        self.seos=seos
        self.x_n=x_n
def aktiivne_any(seos,x_n):#kuna tegu on callablega, siis peab any kas True või False tagastama.
    return
def aktiivne_exists(x_n,seos):
    return not any(x_n,not seos)

#N=input("algmoisteid:")
#K=input("kvantoreid:")

def hulkade_funktsioon1(a, b, c, d):
    return (a in b and b in a) or (c in d and c in a)
def hulkade_funktsioon2(a,b):
    return (a in b and b in b)
def hulkade_funktsioon3(a,b):
    return (a in a)
def hulkade_funktsioon4(a,b,c):
    return (not a in a) and (b in a or c in a)
def kvantoriga_funktsioon(a,b):
    return (a in a)&any(0,lambda x:x in a)

A,B,C=symbols(["A","B","C"])