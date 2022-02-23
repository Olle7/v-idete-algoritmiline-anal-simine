import time
import multiprocessing
from math import log, factorial

def itereeri_üle_Qde_v6_1(Q_min, Q_max, N, _2__N,out):
    aeg=time.time()
    p={}
    for Q in range(Q_min,Q_max):#Q hulga, millesse kuulub järgi indekseerimine võib jõudlust suurendada.
        if Q%1000000==0:
            print(Q,(Q-Q_min)/(Q_max-Q_min),time.time()-aeg)
            aeg = time.time()
        b=0
        grupid={}
        for ix in range(0,N):
            ix_i_tingimus1=Q//_2__N**ix%_2__N
            P2=0
            for j in range(0,N):# ainult osasid bitte P2'est oleks vaja, kui oleks ette teada, et millised P1ed(ixid) gruppikuuluvad.
                P2+=2**j*(not(Q&(1<<(N*j+ix))))
            ix_i_tingimus2=not(Q&(1<<(ix*(N+1))))
            if (ix_i_tingimus1,ix_i_tingimus2) in grupid:
                grupid[(ix_i_tingimus1,ix_i_tingimus2)].add(P2)
            else:
                grupid[(ix_i_tingimus1,ix_i_tingimus2)]=set({P2})
        for välistatud_P2 in grupid.values():
            b+=len(välistatud_P2)#b+=Fq
        ab=(len(grupid),b)
        if ab in p:
            p[ab]+=1
        else:
            p[ab]=1
        #print("Q=",bin(Q),"gruppe on a=",len(grupid),"välistatud veege kokku b=",b)
    out.put(p)
def ridu_v6(N,K, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjeldamiseks
    """
    :param N: Alghulkade, mida seos kirjeldab arv
    :param K: kvantorite "nestedness", ehk kui mitme kvantori sees mingi väide maksimaalselt on.
    :param tohib_teha_kõigi_hulkade_kohta_väiteid: Kas seos tohib teha väiteid, et kõigil hulkadel on mingi omadus. Näiteks, et kõik hulgad on iseenda elemendid.
    :param kvantorid_ei_kehti_alghulkade_kohta: Kas kvanteeritavateks võib asendada ka alghulki.
    :return: Kui palju bitte, selle seose kirjeldamiseks vaja läheb.
    """
    if K==0:
        return 2**(N**2)
    if K!=1:
        raise NotImplementedError
    if kvantorid_ei_kehti_alghulkade_kohta:#analüütilised lahendid
        if tohib_teha_kõigi_hulkade_kohta_väiteid:
            return 2**(N**2+2**(2*N+1))
        else:
            return 2**(N**2)*(2**(2**N)-1)**(2**(N+1))#huvitavad algtegurid!
    #Fqd=[]
    #kui see lihtsustatud saab nii, et enam intereerima ei pea, siis teha sellest generaator.
    if tohib_teha_kõigi_hulkade_kohta_väiteid:
        #p = {}  # ajutine
        _2__N=2**N
        _2__Np1=2**(N+1)
        konstant3=2**(2*N+1)
        aeg=time.time()
        for Q in range(0,2**(N**2-1)):
            if Q%10000==0:
                print(Q,Q/2**(N**2-1),time.time()-aeg)
                aeg = time.time()
            #väistatud_bitte=[0]*(N+1)#ajutine
            b=0
            for P1 in range(0,_2__Np1):
                välistatud_veerud_P1_ja_Q_korral=set()
                for ix in range(0,N):
                    if (not(P1&(1<<ix)))!=(not(P1&(1<<N))):#P1[H(ix) in x]!=P1[x in x] and
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if (not(Q&(1<<(j*N+ix))))==(not(P1&(1<<j))):#Q[H(j) in H(ix)]!=P1[H(j) in x]
                                iga_j_puhul=False
                                break
                        if iga_j_puhul:
                            välistatud_veerud_P1_ja_Q_korral.add(Q//_2__N**ix%_2__N)
                            #print("Q=",Q,"on vastuolus veeruga",P1*(2**N)+P2,"ix=",N-1-ix)
                #print("Q=",Q,"P1=",P1,"korral on vabu bitte",_2__N-len(s))
                #print("Q=",Q,"P1=",P1,"korral on välistatud bitte",len(s))
                #väistatud_bitte[välistatud_bitte_P1_väärtuse_korral]+=1#ajutine
                b+=len(välistatud_veerud_P1_ja_Q_korral)
            #if str(väistatud_bitte) in p:#ajutine
            #    p[str(väistatud_bitte)]+=2#ajutine
            #else:#ajutine
            #    p[str(väistatud_bitte)]=2#ajutine
            #if väistatud_bitte[0]==2**(N+1)-N and väistatud_bitte[1]==N:#ajutine
            #    print(Q,end=",")
            #for k in range(0,len(väistatud_bitte)):#ajutine
            #    print("Q=",Q,"puhul välistas",väistatud_bitte[k],"P1e",k,"bitti")
            sobivaid_ridu+=2**(konstant3-b)
        #print("N=",N)#ajutine
        #for a in sorted(p.keys(),key=lambda x:p[x]):#ajutine
        #    print(p[a],"erineva Q väärtuse puhul:")#ajutine
        #    for k in range(0,len(väistatud_bitte)):#ajutine
        #        print("\tvälistas",ast.literal_eval(a)[k],"erinevat P1 väärtust",k,"veergu")#ajutine
        return sobivaid_ridu*2
    p = {}
    _2__N=2**N

    väljundid=multiprocessing.Queue()
    protsesse=multiprocessing.cpu_count()
    Qsid_protsessis=(2**(N**2-1))//protsesse
    jääk=(2**(N**2-1))%protsesse
    for i in range(0,jääk):
        #print(Qsid_protsessis*i+i,"kuni",Qsid_protsessis*(i+1)+i+1)
        multiprocessing.Process(target=itereeri_üle_Qde_v6_1, args=(Qsid_protsessis*i+i,Qsid_protsessis*(i+1)+i+1,N, _2__N,väljundid)).start()
    for i in range(jääk,protsesse):
        #print(Qsid_protsessis*i+jääk,"kuni",Qsid_protsessis*(i+1)+jääk)
        multiprocessing.Process(target=itereeri_üle_Qde_v6_1, args=(Qsid_protsessis*i+jääk,Qsid_protsessis*(i+1)+jääk,N, _2__N,väljundid)).start()
    for i in range(protsesse):
        väljund=väljundid.get()
        for ab_väljund in väljund.keys():
            if ab_väljund in p:
                p[ab_väljund]+=väljund[ab_väljund]
            else:
                p[ab_väljund]=väljund[ab_väljund]

    sobivaid_ridu=0
    konstant=2**_2__N-1
    _2__Np1=2**(N+1)
    for l in p.keys():
        sobivaid_ridu+=p[l]*konstant**(N-l[0])*2**((l[0]-1)*_2__N+N-l[1])
    #print("N=",N)#ajutine
    #for l in sorted(p.keys(),key=lambda x:p[x]):#ajutine
    #    print(p[l]*2,"erineva Q väärtuse puhul: on ix'ide gruppe a=",l[0],"gruppides on kokku välistatud b=",l[1],"f=",konstant**(N-l[0])*2**((l[0]-1)*_2__N+N-l[1]))#ajutine
    return sobivaid_ridu*konstant**(_2__Np1-N)*2**(_2__N-N+1)


def f3(N,a,b,kd):
    if b==None:#kõikide b'de kohta summaarselt
        n=factorial(2**(N+1))*factorial(N)/factorial(2**(N+1)-a)
        for grupp in range(0,a):
            n/=factorial(kd[grupp])*2**kd[grupp]
        for k in range(1,N+1):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
            n/=factorial(kd.count(k))
        return n
    if b==a:
        n=1
        for grupp in range(0,a):
            n*=(2**a-grupp/2)/factorial(kd[grupp])
        for k in range(1,N+1):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
            n/=factorial(kd.count(k))
        return n*factorial(N)
    else:#VALE
        raise NotImplementedError
        n = 1
        for grupp in range(0,a):
            n*=(2**(b)-grupp/2)*2**(1-kd[grupp]-a+b)/factorial(kd[grupp])
        for k in range(1,N+1):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
            n/=factorial(kd.count(k))
        return n*factorial(N)
def f5(N,a,kde_jaotused):#Ridu uus jaoks vajalik #tagastab, et kui palju on Qsid, milles on a i_x'ide gruppi #vajab sisendiks ka järjendit, mis näitab võimalikke hulkade suurusi.
    Qsid=0
    for k_de_jaotus in kde_jaotused:
        n=factorial(2**(N+1))*factorial(N)/factorial(2**(N+1)-a)
        for k in range(1,N+1):
            #print(str(k)+"seid gruppe on",k_de_jaotus[k-1])
            n/=(2**k*factorial(k))**k_de_jaotus[k-1]*factorial(k_de_jaotus[k-1])
        Qsid+=n
    return Qsid
def ridu_uus(N,K, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjeldamiseks
    """
    Uus ja parem funktsioon, kui POLE VEEL VALMIS. Tahan leida analüütilise lahendi kõigi juhtude jaoks
    :param N: Alghulkade, mida seos kirjeldab arv
    :param K: kvantorite "nestedness", ehk kui mitme kvantori sees mingi väide maksimaalselt on.
    :param tohib_teha_kõigi_hulkade_kohta_väiteid: Kas seos tohib teha väiteid, et kõigil hulkadel on mingi omadus. Näiteks, et kõik hulgad on iseenda elemendid.
    :param kvantorid_ei_kehti_alghulkade_kohta: Kas kvanteeritavateks võib asendada ka alghulki.
    :return: Kui palju bitte, selle seose kirjeldamiseks vaja läheb.
    """


    raise NotImplementedError


print(ridu_v6(1,1)==108)
print(ridu_v6(2,1)==12939750000)
print(ridu_v6(3,1)==22614750144745638013702021260937500000000)
print(ridu_v6(4,1)==57504776229770941169007545256389841736394692150917543524002427730485332894267940532687727065312682987463395495932747329699841284953161621093750000000000000000)
print(ridu_v6(5,1)==34556283262898371093645099183869875566423389568137744895453022122625356133387604707949438614226186417159326907474464038205006178468631108561879313029921057723228155298075946113368807839963526522523031848004262105413688252594807478417249638791195531414955615957022811024209494324264869537391142014818494342036776381097336874580215233971384351214493792797734447459854443760103327596899907701385352204698461218166700448531644768799944040937843949405989305920048801490409137297518208938089771117941360950106749033585130703111215640252037658935139634226202252002613050680828627198934555053710937500000000000000000000000000000000)