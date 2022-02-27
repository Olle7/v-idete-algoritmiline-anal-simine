#import sympy
#from pyparsing import ParseResults
from time import time
from sympy import simplify_logic
#from sympy.abc import symbols
from Seose_parssija import Seose_parssija
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import Equivalent
from pyparsing import ParseResults

#kui kvanteeritav on sama nimega kui alghulk, siis kas:
#    tõlgendada kvantori sees seda kvanteeritavana ja mujal alghulgana
#    või anda veateade, et kvanteeritavat on nimetatud väljaspool kvantorit?

# üledefineerida sümpi booleanavaldise lihtsustamine
# üledefineerida sümpi booleanide vahelised tehted.
# hulkade kuuluvusest automaatselt teha sympy sümbolid.
def tee_väikesed_read(alghulgad,K):#järjekord nr2
    #todo:võiks väikesteks ridadeks võtta ainult need väited, mis seoses sisalduvad.
    väikesed_read=[]
    for alghulk in alghulgad:
        for k in range(1,K+1):
            väikesed_read.append(Symbol(alghulk+"∈"+"x"+str(k)))
    for k in range(1,K+1):
        for alghulk in alghulgad:
            väikesed_read.append(Symbol("x"+str(k)+"∈"+alghulk))
        for k2 in range(1,K+1):
            väikesed_read.append(Symbol("x"+str(k)+"∈x"+str(k2)))
    return väikesed_read
def leia_alghulgad_ja_K(parsitud,k=0,kvanteeritavad=[]):
    k1=k
    k2=k
    if len(parsitud)==2:
        if parsitud[0][0]=="∀":
            kvanteeritav=parsitud[0][1:]
            k1=leia_alghulgad_ja_K(parsitud[1],k+1,kvanteeritavad=kvanteeritavad+[kvanteeritav])
        elif parsitud[0][0]=="∃":
            pass
        else:
            k2=leia_alghulgad_ja_K(parsitud[1],k,kvanteeritavad=kvanteeritavad)
    elif len(parsitud)==3:
        if type(parsitud[0])==str:
            if parsitud[0] not in kvanteeritavad:
                alghulgad.add(parsitud[0])
        else:
            k1=leia_alghulgad_ja_K(parsitud[0],k,kvanteeritavad=kvanteeritavad)
        if type(parsitud[2])==str:
            if parsitud[2] not in kvanteeritavad:
                alghulgad.add(parsitud[2])
        else:
            k2=leia_alghulgad_ja_K(parsitud[2],k,kvanteeritavad=kvanteeritavad)
    else:
        exit("vugane sisend:"+str(parsitud.join("")))
    return max(k1,k2)
def kuva_veerg(veeru_nr):#eerud, mis erinevad ainult selle poolest, et millisele kvanteeritavale on mis tingimus seatud, on samaväärsed. Kui mitu veergu on samaväärsed, siis võib neist ainult ühe tabelisse sisse jätta. Praegu jäävad kõik sisse kahjuks.
    global väikesed_read
    veerg="¬("+"∃("*K
    for i in range(0,len(väikesed_read)):
        if not not veeru_nr & (1<<(len(väikesed_read)-i-1)):
            veerg+="¬"
        veerg+=str(väikesed_read[i])+"∧"
    return veerg[:-1]+")"*K



def parsitust_sympyks(parsitud,kvanteeritavad=[]):#rekusiivne
    global alghulgad,väikesed_read
    print(parsitud,alghulgad,kvanteeritavad)
    if len(parsitud)==1:
        print("?")
        return parsitust_sympyks(parsitud[0])
    elif parsitud[0][0]=="∀" and len(parsitud)==2 and False:#vaja teisendada seoseks veergude vahel.#todo: terve seose K ei ole teada, enne kõigi kvantorite sisude töötlemist. Võiks tagastada mingi objekti, mis on lõplikust Kst sõltumatu. Näiteks seos veeru numbrid eeldusel,et kvanteeritavaid on nii palju, kui selle kvantori sees neid on.
        #siin itereerib üle ainult nende veergude, mis erinevad väikeste ridade poolest, mis kvantori sisus on.
        #exit("pole valmis")
        kvanteeritav=parsitud[0][1:]
        if kvanteeritav in alghulgad:
            print("hoiatus: sama nimega",kvanteeritav,"on nii muutuja kui kvanteeritav")#kvantori sees tõlgendatakse nime kvanteeritavana.
        #kvantori_sisu=simplify_logic(parsitust_sympyks(parsitud[1],kvanteeritavad=kvanteeritavad+[kvanteeritav]))
        kvantori_sisu=parsitust_sympyks(parsitud[1],kvanteeritavad=kvanteeritavad+[kvanteeritav])
        #print(str(kvanteeritav)+"-kvantori sisu on",kvantori_sisu)

#        HÜPOTEES: Mingi(ehk vähemalt ühe) kuuluvusuhte korral x_{n-1}'ga peab x_n tohtima olla mistahes kuuluvusuhtes iseenda, alghulkade ja x_m'idega, kus m<n-1.Seda (eraldi) kõigi x m ’ide ja alghulkade vaheliste kuuluvussuhete puhul. Muidu ei ole Seos kirjeldatud minimaalsetel vabadusastmetel, sest sellise rea tehtud väite teeks ka teistsuguste booleanidega rida.
        #todo:kontrolli, et kas suuremate indeksitega kvanteeritavad ei tee väiteid, mille peaks tegema väiksemate indeksitega kvanteeritavad. Kas seda peaks tegema kvantori sees või peale kogu seose töötlemist?


#        todo:kontrolli, kas väite saaks teha ka väiksema nestednessiga.
#        Kui kvantori sisu ei sõltu kvanteeritava ja ühe võrra väiksema indeksiga kvanteeritava vahelisest kuuluvussuhtest, siis on asi pandav kirja väiksema nestednessiga.
#        kvanteeritava_indeks=len(kvanteeritavad)+1
#        if kvanteeritava_indeks==1:
#            for i in range():
#                if väikesed_read[kvanteeritava_indeks] in kvantori_sisu.free_symbols:#eeldab järjekorda nr2
#                    print("! lihtsustatav ühekordes kvantoriga seoseks.")

        alghulgad_ja_veerud_kvantori_sisus=[]
        väikesed_read_kvantori_sisus=[]
        for väide in kvantori_sisu.free_symbols:
            if väide in väikesed_read:
                väikesed_read_kvantori_sisus.append(väide)
            else:
                alghulgad_ja_veerud_kvantori_sisus.append(väide)
        ülejäänud_väikeste_ridade_nrid=[]
        for i in range(len(väikesed_read)):
            if väikesed_read[i] not in väikesed_read_kvantori_sisus:
                ülejäänud_väikeste_ridade_nrid.append(i)
        #print("seoses olevad väited veegude ja alghulkade kohta:",alghulgad_ja_veerud_kvantori_sisus)
        seos_veergude_vahel=True
        print("itereerida üle",2**len(väikesed_read_kvantori_sisus),"kombinatsiooni.")
        for kombinatsioon in range(0,2**len(väikesed_read_kvantori_sisus)):#veeru välistatav väikeste ridade boolean kombinatsioon on komplement veeru numbrist.
            veeru_nr=0
            #todo:Kas peab sama moodi Q-veergude tingimused leidma? VIST mitte.
            #todo:kontrollida üle, et kas see loogika üldse kehtib. Selleks, et kvantori sisu teeks väiteid alghulkade kohta peab eeldama, et vähemalt 1 hulk eksisteerib.
            veerg_kuhu_väikesed_on_asendatud=kvantori_sisu
            #print("kombinatsioon:",kombinatsioon,bin(kombinatsioon))
            for väike_rida in väikesed_read_kvantori_sisus:
                #print("väikese_rea_nr:",väikesed_read.index(väike_rida))
                #loeb väikeseid ridu teiselt poolt!!!# kui vastav boolean veerus on False
                väikese_rea_nr_sisus=väikesed_read_kvantori_sisus.index(väike_rida)
                väikese_rea_nr=väikesed_read.index(väike_rida)
                väikese_rea_boolean_existentsiaalkvantori_sisus=not kombinatsioon&(1<<(len(väikesed_read_kvantori_sisus)-1-väikese_rea_nr_sisus))
                #print("\t",väikese_rea_nr,väikesed_read[väikese_rea_nr],väikese_rea_boolean_existentsiaalkvantori_sisus)
                if not väikese_rea_boolean_existentsiaalkvantori_sisus:
                    veeru_nr+=2**(len(väikesed_read)-1-väikese_rea_nr)#arvutatakse valesti!
                veerg_kuhu_väikesed_on_asendatud=veerg_kuhu_väikesed_on_asendatud.subs(väike_rida,väikese_rea_boolean_existentsiaalkvantori_sisus)
            #print(kuva_veerg(veeru_nr),veeru_nr, "on jaatatud kui", ~veerg_kuhu_väikesed_on_asendatud)
            for ülejäänud_väikeste_ridade_kombinatsioon in range(2**len(ülejäänud_väikeste_ridade_nrid)):
                täpsem_veeru_nr=veeru_nr
                for j in range(len(ülejäänud_väikeste_ridade_nrid)):
                    if ülejäänud_väikeste_ridade_kombinatsioon&(1<<j):
                        täpsem_veeru_nr+=2**(len(väikesed_read)-1-ülejäänud_väikeste_ridade_nrid[j])
                #print(kuva_veerg(täpsem_veeru_nr), "on jaatatud kui", ~veerg_kuhu_väikesed_on_asendatud)
                seos_veergude_vahel&=~veerg_kuhu_väikesed_on_asendatud>>Symbol("kv"+str(täpsem_veeru_nr))#väikeseid ridu pole seosest seoses.
        #print("kvantor kirjutatud seosteks veergude vahel:",seos_veergude_vahel)
        return seos_veergude_vahel
    elif parsitud[0][0]=="∀" and len(parsitud)==2:#vaja teisendada seoseks veergude vahel.#todo: terve seose K ei ole teada, enne kõigi kvantorite sisude töötlemist. Võiks tagastada mingi objekti, mis on lõplikust Kst sõltumatu. Näiteks seos veeru numbrid eeldusel,et kvanteeritavaid on nii palju, kui selle kvantori sees neid on.
        #siin itereerib üle kõigi veergude.todo: ka siin ei peaks itereeerima ainult üle kõikgi väikesteridadega veergude, sest välimistes kvatorites ei ole sisemiste kvateeritavatega väikseid ridu. Eriti mugav kui saab eeldada, et sisemistes kvantorites pole välimisi kvateeritavaid.
        kvanteeritav=parsitud[0][1:]
        if kvanteeritav in alghulgad:
            print("hoiatus: sama nimega",kvanteeritav,"on nii muutuja kui kvanteeritav")#kvantori sees tõlgendatakse nime kvanteeritavana.
        #kvantori_sisu=simplify_logic(parsitust_sympyks(parsitud[1],kvanteeritavad=kvanteeritavad+[kvanteeritav]))
        kvantori_sisu=parsitust_sympyks(parsitud[1],kvanteeritavad=kvanteeritavad+[kvanteeritav])
        print(str(kvanteeritav)+"-kvantori sisu on",kvantori_sisu)

#        HÜPOTEES: Mingi(ehk vähemalt ühe) kuuluvusuhte korral x_{n-1}'ga peab x_n tohtima olla mistahes kuuluvusuhtes iseenda, alghulkade ja x_m'idega, kus m<n-1.Seda (eraldi) kõigi x m ’ide ja alghulkade vaheliste kuuluvussuhete puhul. Muidu ei ole Seos kirjeldatud minimaalsetel vabadusastmetel, sest sellise rea tehtud väite teeks ka teistsuguste booleanidega rida.
        #todo: kontrolli, et suuremate indeksitega veerg ei teeks väiteid.Kõik väited peaks tegema väikseima indeksitega veerg. See, et kas väide jääba ka suurema indeksiga veerule või mite ei ole sympy formaadis oluline. Selleks tuleb impikatsioonidega näidata, et veerg,väide, mis on ühest liitveerust järeldub oleks ka teistes liitveegudes.
        #for alghulkade_ja_x1_booleankominatsioon:#paneb ainult tasme1 väited tasemele tasemele2
        #    (kvantori_sisu>>~alghulkade_ja_x1_booleankominatsioon)>>~alghulkade_ja_x2_booleankominatsioon
        #for kvanteeritav in kvanteeritavad[1:]:
        #    (kvantori_sisu>>~kvanteeritava_väide)>>~max_kvanteeritavaga_väide#paneb väite õigele tasemele
        #    for kvanteeritav:
        #        (kvantori_sisu>>~kvanteeritava_väide)>>kvanteeritavale_tehtud_järeldus#lisab sisule(teistele kvanteeritavatele) nõuded, mis järelduvad taseme väitest.

#        todo:kontrolli, kas väite saaks teha ka väiksema nestednessiga.
#        Kui kvantori sisu ei sõltu kvanteeritava ja ühe võrra väiksema indeksiga kvanteeritava vahelisest kuuluvussuhtest, siis on asi pandav kirja väiksema nestednessiga.
#        kvanteeritava_indeks=len(kvanteeritavad)+1
#        if kvanteeritava_indeks==1:
#            for i in range():
#                if väikesed_read[kvanteeritava_indeks] in kvantori_sisu.free_symbols:#eeldab järjekorda nr2
#                    print("! lihtsustatav ühekordes kvantoriga seoseks.")

        alghulgad_ja_veerud_kvantori_sisus=[]
        väikesed_read_kvantori_sisus=[]
        for väide in kvantori_sisu.free_symbols:
            if väide in väikesed_read:
                väikesed_read_kvantori_sisus.append(väide)
            else:
                alghulgad_ja_veerud_kvantori_sisus.append(väide)
        #print("seoses olevad väited veegude ja alghulkade kohta:",alghulgad_ja_veerud_kvantori_sisus)
        seos_veergude_vahel=True
        print("itereerida üle",veerge,"veeru")
        for veeru_nr in range(veerge):#veeru välistatav väikeste ridade boolean kombinatsioon on komplement veeru numbrist.
            #todo:Kas peab sama moodi Q-veergude tingimused leidma? VIST mitte.
            #todo:kontrollida üle, et kas see loogika üldse kehtib. Selleks, et kvantori sisu teeks väiteid alghulkade kohta peab eeldama, et vähemalt 1 hulk eksisteerib.
            veerg_kuhu_väikesed_on_asendatud=kvantori_sisu
            for väike_rida in väikesed_read_kvantori_sisus:
                #print("väikese_rea_nr:",väikesed_read.index(väike_rida))
                #loeks väikeseid ridu teiselt poolt, kui max_väikese_rea_nr-väikesed_read.index(väike_rida) asemel oleks väikesed_read.index(väike_rida).
                veerg_kuhu_väikesed_on_asendatud=veerg_kuhu_väikesed_on_asendatud.subs(väike_rida,not(veeru_nr&(1<<(max_väikese_rea_nr-väikesed_read.index(väike_rida)))))
            #print(kuva_veerg(veeru_nr),"on jaatatud kui",~veerg_kuhu_väikesed_on_asendatud)
            seos_veergude_vahel&=~veerg_kuhu_väikesed_on_asendatud>>Symbol("kv"+str(veeru_nr))#väikeseid ridu pole seosest seoses.
        print("kvantor kirjutatud seosteks veergude vahel:",seos_veergude_vahel)
        return seos_veergude_vahel

    elif parsitud[0][0]=="∃" and len(parsitud)==2:#vaja teisendada seoseks veergude vahel.#sisend on parsitud seos väikeste ridade vahel sama kvantori sees.
        exit("pole valmis.")
    elif parsitud[0]=="¬" and len(parsitud)==2:
        return ~parsitud[1]
    elif parsitud[1]=="∈":
        if parsitud[2] in kvanteeritavad:
            if parsitud[0] in alghulgad:
                väikese_rea_nr=K*alghulgad.index(parsitud[0])+kvanteeritavad.index(parsitud[2])#eeldab väikeste ridade järjekorda nr2
                return väikesed_read[väikese_rea_nr]
                #return Symbol(väikese_rea_nr)# kui sympy symbolite asemele panna mingi muu viis booleanfunktsioonide kirjeldamiseks siis saab ka lõppseose vastavas formaadis kirjeldatuna.
            elif parsitud[0] in kvanteeritavad:
                väikese_rea_nr=N*K+kvanteeritavad.index(parsitud[0])*(N+K)+N+kvanteeritavad.index(parsitud[2])#eeldab väikeste ridade järjekorda nr2
                return väikesed_read[väikese_rea_nr]
                #return Symbol("väike rida"+str(väikese_rea_nr))#Sümboli loomise asemel numbrist võib väikesed read ka rea numbri abil järjendist lugeda.
            else:
                exit("booleanid ei tohi hulka kuuluda:",parsitud)
                #return Symbol(väikese_rea_nr)#True või False kuulub alghulka
        elif parsitud[2] in alghulgad:
            if parsitud[0] in kvanteeritavad:
                väikese_rea_nr=N*K+kvanteeritavad.index(parsitud[0])+kvanteeritavad.index(parsitud[0])*(N+K)+alghulgad.index(parsitud[2])#eeldab väikeste ridade järjekorda nr2
                return väikesed_read[väikese_rea_nr]
                #return Symbol("väike rida"+str(väikese_rea_nr))
            elif parsitud[0] in alghulgad:
                #todo:kaaluda ideed panna alghulkade vahelised kuuluvussuhted kirja väites, et hulgad, mis sisaldavad samu elemetnte kui vastav alghulk kuulub alghulka kuhu vastav alghulk kuuluma pidi.
                Qnr=N*alghulgad.index(parsitud[0])+alghulgad.index(parsitud[2])#eeldab et järjestatud A∈A A∈B A∈C B∈A B∈B B∈C C∈A C∈B C∈C
                #Qnr=alghulgad.index(parsitud[0])+N*alghulgad.index(parsitud[2])#eeldab et järjestatud A∈A B∈A C∈A A∈B B∈B C∈B A∈C B∈C C∈C
                #return Symbol(str(Qnr)+parsitud[0]+"∈"+parsitud[2])# kui sympy symbolite asemele panna mingi muu viis booleanfunktsioonide kirjeldamiseks siis saab ka lõppseose vastavas formaadis kirjeldatuna.
                return Symbol("Q"+str(Qnr))#todo:panna sympy asemele mingi efektiivsem süsteem booleanide vahelise seose kirjeldamiseks näiteks DNF ja mingi muu normaalkuju kombinatsioon.#näiteks DNF või CNF, milles on need veerud, mida on seoses, vastavalt tabeli tüübile, kas ainult jaatatud või ainult võitatud.
            else:
                exit("booleanid ei tohi hulka kuuluda:", parsitud)
                #return Qveerg #True või False kuulub alghulka
        else:
            exit("vigane miski: ei saa kuuluda booleani:", parsitud)
    elif parsitud[1]=="∧" and len(parsitud)==3:
        return parsitust_sympyks(parsitud[0],kvanteeritavad)&parsitust_sympyks(parsitud[2],kvanteeritavad)
    elif parsitud[1]=="∨" and len(parsitud)==3:
        return parsitust_sympyks(parsitud[0],kvanteeritavad)|parsitust_sympyks(parsitud[2],kvanteeritavad)
    elif parsitud[1]=="↔" and len(parsitud)==3:
        return Equivalent(parsitust_sympyks(parsitud[0],kvanteeritavad),parsitust_sympyks(parsitud[2],kvanteeritavad))
    elif parsitud[1]=="→" and len(parsitud)==3:
        return parsitust_sympyks(parsitud[0], kvanteeritavad)>>parsitust_sympyks(parsitud[2],kvanteeritavad)
    else:
        exit("vigane sisend:"+str(parsitud))



def to_sympy(seos,tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):
    #Iga kvantoritega seose hulkade vahel saab kirja panna seosena teatud väidete vahelise boolean funktsiooniga. Neid väiteid nimetatakse siin veergudeks, sest kui panna kvantoritega seos DNF tabelina kirja, siis on need väited selle tabeli veerud.

    #jätab alghulkade kuuluvuste vahelised seosed samaks, aga muudab need sympy symboliteks.
    #kvantorid muudab veergude vahelisteks K0seosteks(booleanseosteks).
    #kvantoriveerud muudab sympy sümboliteks.
    #lisab kvantorivvergude omavahelised seosed(et kõigi hulkade kohta väiteid ei teeks) ja kvantoriveergude ning alghulkade vahelised seosed sympy fromaadis seosele.  #Ka DNFiks tegemiseks on iga kvantor vaja asendada veergude, mille tõesust või väärust see nõuab numbritega.
    #lõpuks laseb sympyl sympy sümbolite vahelise seose lihtsustada.

    #todo:kui erinevate seoste vahel booleanoperaatoreid rakendatakse peab seos ise aru saama, et sama numbriga kvantoriveerud tähistavad erinevaid veergusi kui seoste alghlgad või K on erinevad.
    global alghulgad,N,K,väikesed_read,veerge,max_väikese_rea_nr
    if type(seos)!=ParseResults:
        seos = Seose_parssija.parseString(seos)[0]
    alghulgad = set()
    K=leia_alghulgad_ja_K(seos)
    print("K=",K)
    N=len(alghulgad)
    max_väikese_rea_nr=K*(K+2*N)-1
    alghulgad=sorted(alghulgad)
    väikesed_read=tee_väikesed_read(alghulgad, K)
    veerge=2**(K*(K+2*N))
    print(väikesed_read)
    seos=parsitust_sympyks(seos)
    for veerg in seos.free_symbols:
        if veerg.name[0]=="Q":
            nr=int(veerg.name[1:])
            veerg.name=alghulgad[nr//N]+"∈"+alghulgad[nr%N]
        elif veerg.name[0]=="k":
            veerg.name=kuva_veerg(int(veerg.name[2:]))
    del alghulgad,veerge,K,N,väikesed_read
    print("seos sympys:",seos)
    #input()

    #kirjutab read, kus kvanteeritav ei sõltu ühe võrra väiksemast kvanteritavas, ümber.
    if not tohib_teha_kõigi_hulkade_kohta_väiteid:
        #lisab seosed, mis kinnitavad, et kõikide erinevate omadustega hulgad on olema.#Seosed ainult nende kvantoriveergude kohta, mida on seose kirjeldamiseks kasutatud.
        pass
    if not kvantorid_ei_kehti_alghulkade_kohta:
        #todo:lisab seosed kvantorite ja alghulkade vahel. #Seosed ainult nende kvantoriveergude kohta, mida on seose kirjeldamiseks kasutatud.
        pass
    #kotrollib ,et madalama taseme seoseid ei tehaks kõrgemal tasemel.
    return seos#ajutine
    return simplify_logic(seos)
def to_DNF_int():
    pass
def to_int(seos, pakitus):
    pass

aeg=time()
#print(to_sympy("C∈A∧∀x(x∈D∧∀y(y∈x))∨(¬A∈A∧A∈B∧A∈C∧C∈C↔¬(B∈B∧B∈C))∨∀x1(x1∈A∧B∈B)"))
#print(to_sympy("B∈A∨∀x1(x1∈B∨x1∈A)"))
#print(to_sympy("∀x(A∈x∧x∈B∧∀y(y∈x∧y∈A))"))
#print(to_sympy("∀x(x∈A∨A∈A)"))
to_sympy("∀x(x∈A→x∈B)")
def kuva_veerg2(veeru_nr,K,N):#veerud, mis erinevad ainult selle poolest, et millisele kvanteeritavale on mis tingimus seatud, on samaväärsed. Kui mitu veergu on samaväärsed, siis võib neist ainult ühe tabelisse sisse jätta. Praegu jäävad kõik sisse kahjuks.
    global väikesed_read
    veerg="¬"+"∃("*K
    for k in range(0,K):
        #g_väärtus=
        exit("pole valmis")
        veerg+="g(Q,x"+str(k)+")="+str(g_väärtus)+")∧"
    return veerg[:-1]+")"*K
print(kuva_veerg2(0,K=1,N=1))
#print(to_sympy("∀x(x∈A→∀y(y∈x))"))

#with open("sisendid/naturaalarvud") as fail:
#    naturaalarvude_seos=to_sympy(fail.read())
#seos1=to_sympy("B∈A ∧ ∀x(x∈A)")
#seos2=to_sympy("A∈B∧∀y(y∈B)")
#seos3=to_sympy("∀x1(x1∈A∧x1∈B)∧A∈B∧B∈A")
#print((seos1&seos2)==seos3)

print("aega kulus:",time()-aeg)