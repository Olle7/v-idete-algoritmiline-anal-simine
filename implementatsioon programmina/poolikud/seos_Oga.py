#TODO: jaatatud universaalsuskvantorid koku panna?
def asenduste_valikud(võimalikke_väärtusi):
    num=[]
    for i in võimalikke_väärtusi:
        if i==None:
            num.append(-1)
        else:
            num.append(0)
    while True:
        yield num
        for i in range(0,len(võimalikke_väärtusi)):
            if num[i]==võimalikke_väärtusi[i]:
                num[i]=0
            elif võimalikke_väärtusi[i]!=None:
                num[i]+=1
                break
        else:
            return

#for i in asenduste_valikud([]):
#    print(i)
#input()

from copy import deepcopy, copy
from sympy import Symbol, to_dnf, Or, And, Not, S
#TODO:Et performany parendada võib Sympyst ainult need asjad oma projekti kopeerida, mida kasutan ja liigsed väljad kustutada.

#TODO:kui ainult predikaadid, NOR ja U on pole sympit enam vb. vaja. Ülejäänud seose enda sees defineeritud.
class Predikaat_väide(Symbol):#võib symbol asemel pärineda Atomist või Booleanist.
    def __new__(self, nimi, argumendid=[]):
        predikaat_väide=Symbol.__new__(self, nimi+"("+','.join([str(i) for i in argumendid])+")")
        predikaat_väide.argumendid=argumendid
        predikaat_väide.nimi=nimi
        predikaat_väide.eitamta=True
        return predikaat_väide
class Predikaat:
    def __init__(self,nimi):
        self.nimi=nimi
    def __call__(self, *args, **kwargs):
        return Predikaat_väide(self.nimi,args)
class Plato(Symbol):#TODO: ei pea laiendama klassi symbol.
    def __new__(self, sisu):
        assert type(sisu)==tuple and len(sisu)==3
        Plato=Symbol.__new__(self,self.nimi(sisu[0],sisu[1],sisu[2]))
        Plato.predikaadid=sisu[0]
        Plato.universaalsus_osa=sisu[1]
        Plato.eksistentsiaalsus_osa=sisu[2]
        return Plato
    def u_lõpuni(self,u_sisu=S.true):#TODO: saab vist nii teha, et kohe universaalsus_osa juba sisaldaks rekusiivselt kõrgemal olevat.
        u_sisu&=self.predikaadid
        if self.universaalsus_osa!=True:
            u_sisu&=self.universaalsus_osa.u_lõpuni()
        return u_sisu
    def ue_jooned(self,paaris=True):#TODO: iga Plato puhul salvestatakse, et mida ta paaris ja paaritul läbimisel tagastama hakkab.
        #TODO:pole vaja märgendit, et kas JA või VÕI. Saab ka indeksi järgi järeldada.
        if paaris:
            v=[True]
            if self.universaalsus_osa!=True:
                for joon in self.universaalsus_osa.ue_jooned(paaris):
                    v.append(self.predikaadid&joon)
            elif self.eksistentsiaalsus_osa:
                for k in self.eksistentsiaalsus_osa:
                    for joon in self.k._args[0].ue_jooned(not paaris):
                        v.append(self.predikaadid&joon)
            else:
                v.append(self.predikaadid)
        else:
            v=[False]
            if self.universaalsus_osa!=True:
                for joon in self.universaalsus_osa.ue_jooned(paaris):
                    v.append(self.predikaadid&joon)
            for k in self.eksistentsiaalsus_osa:
                for joon in self.k._args[0].ue_jooned(not paaris):
                    v.append(self.predikaadid&joon)
        return v
    @staticmethod
    def nimi(p,u,e):
        s="("
        if p:
            s+=str(p[0])
        for predikaat in p[1:]:
            s+=" & "+str(predikaat)+""
        if u:
            if p:
                s+="&"
            s+="¬∃("+str(u[0])+")"
        for uk in u[1:]:
            s+="&¬∃("+str(uk)+")"
        if e:
            if p or u:
                s+="&"
            s+="∃("+str(e[0])+")"
        for ek in e[1:]:
            s+="&∃("+str(ek)+")"
        return s+")"
    #def nimeta(self):
    #    self.name=self.nimi(self.predikaadid,self.universaalsus_osa,self.eksistentsiaalsus_osa)
class E(Symbol):#TODO: võiks ka funktsioon olla, mis kohe lihtsustatud vormi tagastab(sama, mis mitte_ÜV praegu).
    def __new__(self,sisu):
        E=Symbol.__new__(self,"∃("+str(sisu)+")")
        E.sisu=sisu
        return E

def jaota_osadesse(boolean_väide):
    boolean_väide=to_dnf(boolean_väide.simplify(),True)
    if type(boolean_väide)==Or:
        boolean_väide=boolean_väide.args
    else:
        boolean_väide=[boolean_väide]
    for dnf_element in boolean_väide:
        if type(dnf_element) == And:
            sisu=dnf_element.make_args(dnf_element)
        else:
            sisu=[dnf_element]
        predikaadid=[]
        universaalsus_osa=[]
        eksistentsiaalsus_osa=[]
        for jaatuse_element in sisu:
            tüüp=type(jaatuse_element)
            if tüüp==E:
                eksistentsiaalsus_osa.append(jaatuse_element)
            elif tüüp==Not:
                if type(jaatuse_element._args[0]) == E:
                    universaalsus_osa.append(jaatuse_element._args[0])#TODO:peaks sisemiselt, mitte väliselt eitama.
                    #TODO: kuna 2 kordne sisemine eitus annab sama tulemuse saab lihtsalt 2 vormi salvestada(ilma koopiata sisust).
                    #TODO: Et Eksistentsiaalsuskvantoreid peab sisemiselt eitama võib ka o-tingimuste kotrollis arvestada. Teades ainult, kas oled läinud paaris või paaritu arvu eksistentsiaalsuskvantorite sisse.
                else:
                    assert type(jaatuse_element._args[0])==Predikaat_väide
                    jaatuse_element._args[0].eitamata=False
                    predikaadid.append(jaatuse_element._args[0])
            else:
                assert tüüp==Predikaat_väide
                predikaadid.append(jaatuse_element)
        yield (predikaadid,universaalsus_osa,eksistentsiaalsus_osa)

def mitte_ÜV(seos, k=0):#TODO:kui laiendada Expr klassi siis saab selle ehk klassimeetodiks teha.
    sisemised_kvantorid=[]
    sisemiste_kvantorite_võitatud_vormid=[]
    for sisemine_kvantor in seos.atoms():
        if type(sisemine_kvantor)==E:
            sisemised_kvantorid.append(sisemine_kvantor)
            sisemiste_kvantorite_võitatud_vormid.append(mitte_ÜV(sisemine_kvantor.sisu,k+1))
    #print(seos, " :sisemiste_kvantorite_võitatud_vormid:", sisemiste_kvantorite_võitatud_vormid)
    #print("type:", type(seos), "; plato:", seos, ";")
    võitatud_vormid=[]
    for sisemise_võituse_elemendi_p_osa,sisemise_võituse_elemendi_u_osa,sisemise_võituse_elemendi_e_osa in jaota_osadesse(seos):
        for i_sisemine_kvantor in range(len(sisemise_võituse_elemendi_u_osa)):#teeb asendused U-osas.
            #TODO:PEAB need üheks kvantoriks ühendama, et saaks teada, kas midagi saab kõrgemalt alla poole tuua.
            eitatud_ek=sisemise_võituse_elemendi_u_osa.pop(0)
            #print("    eitatud kvantor:",eitatud_ek)
            for variant in sisemiste_kvantorite_võitatud_vormid[sisemised_kvantorid.index(eitatud_ek)]:
                sisemise_võituse_elemendi_u_osa.append(variant)
                #print("      u-ossa lisada:",variant)

        asenduste_valik=[None]*len(sisemised_kvantorid)
        for sisemine_kvantor in sisemise_võituse_elemendi_e_osa:#määrab, et kui palju variante kui mitmenda kvantori asendamiseks E-osas on.
            i=sisemised_kvantorid.index(sisemine_kvantor)
            asenduste_valik[i]=len(sisemiste_kvantorite_võitatud_vormid[i])-1
        for asenduste_valik in asenduste_valikud(asenduste_valik):
            välimise_võituse_elemendi_e_osa=[]
            for i in range(len(asenduste_valik)):#TODO: asendada ainult muutunud indeksitega(asenduste valikus) kvantorid.
                if asenduste_valik[i]!=-1:#kõik ja ainult U'd asendatakse mingi Plato'e või predikaatide vahelise booleanseosega.
                    #print("    asendada:",sisemised_kvantorid[i],":",sisemiste_kvantorite_võitatud_vormid[i][asenduste_valik[i]])
                    välimise_võituse_elemendi_e_osa.append(sisemiste_kvantorite_võitatud_vormid[i][asenduste_valik[i]])
            #TODO: predikaatide ja platode, mis ei sisalda mingi kvantori kvanteeritavat, sellest kvantorist välja viimine on o kontrolliks vajalik.

            for kvantor in välimise_võituse_elemendi_e_osa:#TODO: saaks ka iga plato kõrvale lihtsalt tema o1-muundatud vormi salvestada.
                for haru in kvantor.eksistentsiaalsus_osa:
                    muundatud=o1_muunda(haru,k+1)
                    #print("e-haru",haru,"o1-töötlus(eemaldada: x_"+str(k+1)+"):",muundatud)
                    välimise_võituse_elemendi_e_osa.append(muundatud)
                for haru in kvantor.universaalsus_osa:
                    muundatud=o1_muunda_u(haru,k+1)#TODO: eitatud harudesse tuleb x_{k+1} asemele asendada False, ehk kui see on jaatustega vormis, siis tuua madalamale tasemele ainult need, mis ei sisalda x_{k+1}'e.
                    #print("e-haru",haru,"o1-töötlus(eemaldada: x_"+str(k+1)+"):",muundatud)
                    välimise_võituse_elemendi_e_osa.append(muundatud)
            #TODO: teistipidi o-muundatud variant tuleb just eitatud_ossa(u_ossa) sisse viia. Seda rekusiivselt pannes igal tasemel ette eituse ja eemaldades sisemised kvanteeritavad. Peale seda tuleb o-tingimused platos uuesti üle kontrollida.
            #TODO: ka u_osast tuleks o1-muundatud elemente välja tuua.
            välimise_võituse_element=Plato((sisemise_võituse_elemendi_p_osa,sisemise_võituse_elemendi_u_osa,välimise_võituse_elemendi_e_osa))

            #TODO:optimeerimiseks saaks kontrollida, et kas on haruid, mille sisu on mõne teise haru sisust järelduv ja need eemaldada.

            #print("VVE:",välimise_võituse_element)
            if o2(välimise_võituse_element):
                võitatud_vormid.append(välimise_võituse_element)
    print("  võitatud vormid:",võitatud_vormid)
    if võitatud_vormid:
        return võitatud_vormid
    return [False]
def o2(välimise_võituse_element):
    return True
def o1_muunda(haru,k):#TODO: teha see klassi Plato meetodiks.
    predikaadid=[]
    for predikaat in haru.predikaadid:
        töödeldud_argumendid=[]
        for argument in predikaat.argumendid:
            if argument==k:
                break
            elif argument>k:
                töödeldud_argumendid.append(argument-1)
            else:
                töödeldud_argumendid.append(argument)
        else:
            predikaadid.append(Predikaat_väide(predikaat.nimi,töödeldud_argumendid))
    universaalsus_osa=[]
    for kvantor in haru.eitatud_EKd:#TODO:kas universaalsuskvantorist saab samamoodi eemaldada?
        universaalsus_osa.append(o1_muunda(kvantor,k))
    eksistentsiaalsus_osa=[]
    for kvantor in haru.EKd:
        eksistentsiaalsus_osa.append(o1_muunda(kvantor,k))
    return Plato((predikaadid,universaalsus_osa,eksistentsiaalsus_osa))




if __name__=="__main__":
    on_null=Predikaat("on_null")
    võrdne=Predikaat("võrdne")
    PEANO=E(on_null(1))&\
          ~E(~võrdne(1,1))&\
          ~E(E(E(~((võrdne(1,2)&võrdne(2,3))>>võrdne(3,1)))))
    print("Peano tulem:",mitte_ÜV(PEANO))
    print("\n#####\n")

    A=Predikaat("A")
    print(mitte_ÜV(E(A(1)&A(1,1)&E(A(1,2)&E(A(2,3)&A(3,1))))))

    if True:# võituste välja viimine ilma o-kontrolliteta.
        print("################################\nTESTS:")
        sisendid=[~E(A(21)&A(22)&A(23)),E(E(E(E(A(0)|A(1)|A(2))))),(E(A(30)&A(31))|(A(33)&E(A(40)|A(41)&E(E(E(A(51)|A(53))))))),~E(A(1)&A(2)),
                  ~E(A(1) | A(2) & A(3)) & E(A(4) & A(5) & E(A(6))),
                  A(10)&E(A(11)>>A(12)&~E(A(13)|A(14)&~E(A(10)&A(20)))),
                  E(võrdne(0)&on_null(2)&on_null(1)),
                  ~E(A(2)<<A(1)),E(A(1) | A(2)) & E(A(1) | A(2))]
        oodatud=["[(¬∃((A(21) & A(22) & A(23))))]",
                 "[(∃((∃((∃((∃((A(0)))))))))), (∃((∃((∃((∃((A(1)))))))))), (∃((∃((∃((∃((A(2))))))))))]",
                 "[(∃((A(30) & A(31)))), (A(33)&∃((A(40)))), (A(33)&∃((A(41)&∃((∃((∃((A(51)))))))))), (A(33)&∃((A(41)&∃((∃((∃((A(53))))))))))]",
                 "[(¬∃((A(1) & A(2))))]",
                 "[(¬∃((A(1)))&¬∃((A(2) & A(3)))&∃((A(4) & A(5)&∃((A(6))))))]",
                 "[(A(10)&∃((A(12)&¬∃((A(13)))&¬∃((A(14)&¬∃((A(10) & A(20)))))))), (A(10)&∃((~A(11)&¬∃((A(13)))&¬∃((A(14)&¬∃((A(10) & A(20))))))))]",
                 "[(∃((on_null(1) & on_null(2) & võrdne(0))))]",
                 "[(¬∃((A(2)))&¬∃((~A(1))))]",
                 "[(∃((A(1)))), (∃((A(2))))]"]
        for i in range(max(len(sisendid),len(oodatud))):
            tulemus=str(mitte_ÜV(sisendid[i]))
            if tulemus!=oodatud[i]:
                print("SISEND :",sisendid[i])
                print("TULEMUS:",tulemus)
                print("OODATUD:",oodatud[i])
                print()
                #print(sisendid[i],":",tulemus,":",oodatud[i])
        # proov=mitte_ÜV(U(A(0)&A(1)&U(A(3)&A(4)&U(A(5)))&~U(A(21)&A(22)&U(A(23))&~U(A(24)|A(25)))))
        # print("proov:",mitte_ÜV(U(U(on_null(2))&U(võrdne(2,2)))))
        # proov2=mitte_ÜV(U(U(U(U(A(0)&A(1)&A(2))))))
        # proov2=mitte_ÜV(~U(A(0) | A(1) | A(2)))
        # print("proov:", proov2)
    if False:
        assert not mitte_ÜV(E(A(1,1)&~E(~(A(2,2)&~A(1,2)&~A(2,1)))))#tegelt ÜV
        assert not mitte_ÜV(E(A(1, 1)&U(A(2, 2)>>~A(1, 2)&~A(2, 1))))#tegelt ÜV
        assert (mitte_ÜV(U(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))&E(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))))#tegelt ÜV