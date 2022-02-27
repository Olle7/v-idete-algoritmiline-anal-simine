#Ei ole parem kui failis soseos.py olev, sest universaalsuskvantorite sisse tuleks võitused ja eksistentsiaalsuskvantoritesse jaatused. ue-joonte leidmine sama raske kui failis seos_Oga.py oleva algoritmiga.
#Optimeerimis-kommentaarid failis seos_Oga.py
from sympy import Symbol, to_dnf,to_cnf, Or, And, Not, S
class U(Symbol):
    def __new__(self,sisu):
        U=Symbol.__new__(self,"∀("+str(sisu)+")")
        U.sisu=sisu
        return U

class E:#kasutaja ei saa seda sisestada. Töötlemiseks kasutada ainult
    def __init__(self,u):
        assert type(u)==Not
        self.sisu=~u._args[0].sisu
    def __str__(self):
        return "e("+str(self.sisu)+")"

class Töödeldud_plato(Symbol):#TODO: ei pea laiendama klassi symbol.
    def __new__(self,nimi):
        u2=Symbol.__new__(self,nimi)
        u2.predikaadid=S.true
        u2.universaalsus_osa=S.true
        u2.E_kvantorid=[]
        return u2
    @staticmethod
    def nimi(p,u,e):
        s="("
        if p!=True:
            s+=str(p)
        if u!=True:
            if p!=True:
                s+="&"
            s+="∀("+str(u)+")"
        if e and (u!=True or p!=True):
            s+="&∃("+str(e[0])+")"
        for ek in e[1:]:
            s+="&∃("+str(ek)+")"
        return s+")"
    def nimeta(self):
        self.name=self.nimi(self.predikaadid, self.universaalsus_osa, self.E_kvantorid)


def asenda_E_notU_asemele(plato):
    #sisemised_kvantorid=[]
    #sisemiste_kvantorite_võitatud_vormid=[]
    plato=to_dnf(plato.simplify())
    if type(plato)==Or:
        plato=plato.make_args(plato)
    else:
        plato=[plato]
    vormid=[]
    for dnf_element in plato:
        print("dnf_element:",dnf_element)
        töödeldud_plato=Töödeldud_plato(str(dnf_element))
        if type(dnf_element)==And:
            dnf_element=dnf_element.make_args(dnf_element)
        else:
            dnf_element=[dnf_element]
        for or_element in dnf_element:
            if type(or_element)==Not and type(or_element._args[0])==U:
                töödeldud_plato.E_kvantorid.append(E(or_element))
            else:
                töödeldud_plato.universaalsus_osa&=or_element
        töödeldud_plato.nimeta()
        print("lisada:",töödeldud_plato)
        vormid.append(töödeldud_plato)
    return vormid


def mitte_ÜV(plato,k=0):
    print("plato:", plato)
    töödeldud_plato=asenda_E_notU_asemele(plato)
    #print(type(töödeldud_plato.E_kvantorid[0]))
    print("töödeldud plato:",töödeldud_plato)
    #TODO:Mitte unustada, et universaalsuskvantoritest võitusi välja ei tuua.