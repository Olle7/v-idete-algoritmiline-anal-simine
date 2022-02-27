import time
import multiprocessing
import ast
from math import log, factorial
def ridu_v2(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjleoda miseks dnf formaadis.#K=1#eeldab, et kvantorid ei kehti algmõistete kohta.
    if kvantorid_ei_kehti_alghulkade_kohta:#analüütilised lahendid
        if tohib_teha_kõigi_hulkade_kohta_väiteid:
            return 2**(N**2+2**(2*N+1))
        else:
            return 2**(N**2)*(2**(2**N)-1)**(2**(N+1))#huvitavad algtegurid!
    sobivaid_ridu=0
    #Fqd=[]
    #kui see lihtsustatud saab nii, et enam intereerima ei pea, siis teha sellest generaator.
    if tohib_teha_kõigi_hulkade_kohta_väiteid:
        for Q in range(0,2**(N**2)):
            if Q % 1000 == 0:
                print(Q)
            #print("Q=",bin(Q))
            Fq=0
            for nv in range(0,2**(2*N+1)):
                for ix in range(0,N):
                    iga_j_puhul=False
                    #print(bin(int(Q*2**(N*ix+N-N**2))%(2**N)),bin(nv%(2**N)),"Q=",Q,"nv=",nv,"ix=",ix)
                    if int(Q*2**(ix+N*ix+1-N**2))%2!=int(nv*2**(-2*N))%2 and 0==nv%(2**N)^(~int(Q*2**(N*ix+N-N**2))%(2**N)):
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if not int(Q*2**(j*N+ix+1-N**2))%2!=int(nv*2**(j+1-2*N))%2:
                                iga_j_puhul=False
                                break
                    if iga_j_puhul:
                        Fq+=1
                        #print("Q=",Q,"on vastuolus veeruga",nv,"ix=",ix)
                        break
            #print(Fq,end=";")
            #Fqd.append(Fq)
            sobivaid_ridu+=2**(2**(2*N+1)-Fq)
        #print(Fqd.count(0),Fqd.count(1),Fqd.count(2),Fqd.count(3),Fqd.count(4))
        return sobivaid_ridu
    p = {}  # ajutine

    _2__N=2**N
    _2__Np1=2**(N+1)
    aeg=time.time()
    for Q in range(0,2**(N**2-1)):
        if Q%10000==0:
            print(Q,Q/2**(N**2-1),time.time()-aeg)
            aeg = time.time()
        väistatud_bitte=[0]*(N+1)#ajutine
        ridu_Q_väärtuse_korral=1
        for P1 in range(0,_2__Np1):
            välistatud_bitte_P1_väärtuse_korral=0
            for P2 in range(0,_2__N):#nv=P1+P2*2**(N+1)
                for ix in range(0,N):
                    if (not(P1&(1<<ix)))!=(not(P1&(1<<N))) and not P2^~Q//_2__N**ix%_2__N:#P1[H(ix) in x]!=P1[x in x] and
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if (not(Q&(1<<(j*N+ix))))==(not(P1&(1<<j))):#Q[H(j) in H(ix)]!=P1[H(j) in x]
                                iga_j_puhul=False
                                break
                        if iga_j_puhul:
                            välistatud_bitte_P1_väärtuse_korral+=1
                            #print("Q=",Q,"on vastuolus veeruga",P1*(2**N)+P2,"ix=",N-1-ix)
                            break
            vabu_bitte_P1_väärtuse_korral=_2__N-välistatud_bitte_P1_väärtuse_korral
            #print("Q=",Q,"P1=",P1,"korral on vabu bitte",vabu_bitte_P1_väärtuse_korral)
            #print("Q=",Q,"P1=",P1,"korral on välistatud bitte",välistatud_bitte_P1_väärtuse_korral)
            väistatud_bitte[välistatud_bitte_P1_väärtuse_korral]+=1#ajutine
            if välistatud_bitte_P1_väärtuse_korral==0:
                ridu_Q_väärtuse_korral*=(2**vabu_bitte_P1_väärtuse_korral)-1
            else:
                ridu_Q_väärtuse_korral*=2**vabu_bitte_P1_väärtuse_korral

        if str(väistatud_bitte) in p:#ajutine
            p[str(väistatud_bitte)]+=2#ajutine
        else:#ajutine
            p[str(väistatud_bitte)]=2#ajutine
        #if väistatud_bitte[0]==2**(N+1)-N and väistatud_bitte[1]==N:#ajutine
        #    print(Q,end=",")
        #for k in range(0,len(väistatud_bitte)):#ajutine
        #    print("Q=",Q,"puhul välistas",väistatud_bitte[k],"P1e",k,"bitti")
        sobivaid_ridu+=ridu_Q_väärtuse_korral
    #print("N=",N)#ajutine
    #for a in sorted(p.keys(),key=lambda x:p[x]):#ajutine
    #    print(p[a],"erineva Q väärtuse puhul:")#ajutine
    #    for k in range(0,len(väistatud_bitte)):#ajutine
    #        print("\tvälistas",ast.literal_eval(a)[k],"erinevat P1 väärtust",k,"veergu")#ajutine
    return sobivaid_ridu*2
def veerge(N,tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#K=1#eeldab, et kvantorid ei kehti algmõistete kohta.
    return log(ridu_v2(N, tohib_teha_kõigi_hulkade_kohta_väiteid=tohib_teha_kõigi_hulkade_kohta_väiteid, kvantorid_ei_kehti_alghulkade_kohta=kvantorid_ei_kehti_alghulkade_kohta), 2)


#print(ridu(1)==108)
#print(ridu(2)==12939750000)
#print(ridu(3)==22614750144745638013702021260937500000000)
#print(ridu(4)==57504776229770941169007545256389841736394692150917543524002427730485332894267940532687727065312682987463395495932747329699841284953161621093750000000000000000)
#print(ridu(5))

def ridu_v0(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):
    sobivaid_ridu=0
    nR=0
    aeg=time.time()
    rida_üheselt_vale=False
    while nR<2**(2**(2*N+1)+N**2):
        rida_üheselt_vale=False
        if nR%100000==0:
            print(nR,nR/2**(2**(2*N+1)+N**2), time.time()-aeg)
            aeg=time.time()
        if not tohib_teha_kõigi_hulkade_kohta_väiteid:
            for i in range(0,2**(N+1)):
                if int(nR*2**(-N**2-i*2**N))%2**(2**N)==2**(2**N)-1:
                    #print(nR,"on üheselt vale, sest teeb kõigi hulkade kohta väite.")
                    rida_üheselt_vale=True
                    nR+=2**(i*2)-1#See rida on ainult optimiseerimiseks. Väljund ei sõltu sellest.
                    break
        if not rida_üheselt_vale and not kvantorid_ei_kehti_alghulkade_kohta:# and not kvantorid_ei_kehti_alghulkade_kohta:
            for nv in range(0,2**(2*N+1)):
                if int(nR*2**(nv+1-N**2-2**(2*N+1)))%2==1:
                    for ix in range(0,N):
                        iga_j_puhul=False
                        if int(nR*2**(ix+N*ix+1-N**2))%2!=int(nv*2**(-2*N))%2 and nv%(2**N)!=int(nR*2**(N*ix+N-N**2))%(2**N):
                            iga_j_puhul=True
                            for j in range(0,N):#iga j puhul peab tõene olema.
                                if not int(nR*2**(j*N+ix+1-N**2))%2!=int(nv*2**(j+1-2*N))%2:
                                    iga_j_puhul=False
                                    break
                    if iga_j_puhul:
                        rida_üheselt_vale=True
                        #print(nR,"on üheselt vale, sest alghulkde veergudest järelduv on kvantoriveergudest järelduvaga vastuolus.")
                        break
        if not rida_üheselt_vale:
            sobivaid_ridu+=1
        nR+=1
    return sobivaid_ridu

def leia_üheselt_valed_read(N):
    nR = 0
    sobivaid_ridu = 0
    #    aeg=time.time()
    c0=2**(2**(2*N+1)+N**2)
    c1=2**(N+1)
    c2=2**(2**N)
    c3=2**(2**N)-1
    c4=2**(2*N+1)
    c5=1-N**2-2**(2*N+1)
    c6=1-N**2
    c7=2**(-2*N)
    c8=2**N
    c9=N**2
    c10=1-2*N
    while nR < c0:
        rida_üheselt_vale = False
        # if nR%100000==0:
        #    print(nR,nR/2**(2**(2*N+1)+N**2), time.time()-aeg)
        #    aeg=time.time()
        for i in range(0, c1):
            if int(nR * 2 ** (-c9 - i * c8)) % c2 == c3:
                # print(nR,"on üheselt vale, sest teeb kõigi hulkade kohta väite.")
                rida_üheselt_vale = True
                yield nR
                #nR += 4 ** i - 1  # See rida on ainult optimiseerimiseks. Väljund ei sõltu sellest.
                break
        if not rida_üheselt_vale:  # and not kvantorid_ei_kehti_alghulkade_kohta:
            for nv in range(0, c4):
                if int(nR * 2 ** (nv + c5)) % 2:
                    for ix in range(0, N):
                        iga_j_puhul = False
                        if int(nR * 2 ** (ix + N * ix + c6)) % 2 != int(nv * c7) % 2 and (nv % c8) != int(
                                        nR * c8 ** (ix + 1 - N)) % c8:
                            iga_j_puhul = True
                            for j in range(0, N):  # iga j puhul peab tõene olema.
                                if not int(nR * 2 ** (j * N + ix + c6)) % 2 != int(nv * 2 ** (j + c10)) % 2:
                                    iga_j_puhul = False
                                    break
                    if iga_j_puhul:
                        #rida_üheselt_vale = True
                        yield nR
                        # print(nR,"on üheselt vale, sest alghulkde veergudest järelduv on kvantoriveergudest järelduvaga vastuolus.")
                        break
        nR+=1

#    : õige,tohib teha kõigi hulkade kohta väiteid,kvatorid ei kehti alghulkadele,kõik read
#N=1 : 108,256,162,512
#N=2 : 12939750000,41006250000,19327352832,68719476736
#N=3 : 22614750144745638013702021260937500000000,23819765684465692442436222520223774801920,163648808609320185659789125078125000000000,174224571863520493293247799005065324265472
#N=4 : 57504776229770941169007545256389841736394692150917543524002427730485332894267940532687727065312682987463395495932747329699841284953161621093750000000000000000,?,?,?

#from sympy.ntheory import factorint
#i=0
#while True:
#    i+=1
#    print(leia_vastuolulisi_ridu(i,kvantorid_ei_kehti_alghulkade_kohta=True,tohib_teha_kõigi_hulkade_kohta_väiteid=True),end=" , ",flush=True)
#    print(leia_vastuolulisi_ridu(i,kvantorid_ei_kehti_alghulkade_kohta=True,tohib_teha_kõigi_hulkade_kohta_väiteid=False),end=" , ",flush=True)#huvuitavad algtegurid!
#    print(leia_vastuolulisi_ridu(i,kvantorid_ei_kehti_alghulkade_kohta=False,tohib_teha_kõigi_hulkade_kohta_väiteid=True),end=" , ",flush=True)
#    print(leia_vastuolulisi_ridu(i),flush=True)
    #print(factorint(leia_vastuolulisi_ridu(i)))

def ridu_v1(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#osaliselt optimiseeitud.
    if kvantorid_ei_kehti_alghulkade_kohta:#analüütilised lahendid
        if tohib_teha_kõigi_hulkade_kohta_väiteid:
            return 2**(N**2+2**(2*N+1))
        else:
            return 2**(N**2)*(2**(2**N)-1)**(2**(N+1))#huvitavad algtegurid!
    sobivaid_ridu=0
    #Fqd=[]
    if tohib_teha_kõigi_hulkade_kohta_väiteid:
        for Q in range(0,2**(N**2)):
            if Q % 1000 == 0:
                print(Q)
            #print("Q=",bin(Q))
            Fq=0
            for nv in range(0,2**(2*N+1)):
                for ix in range(0,N):
                    iga_j_puhul=False
                    #print(bin(int(Q*2**(N*ix+N-N**2))%(2**N)),bin(nv%(2**N)),"Q=",Q,"nv=",nv,"ix=",ix)
                    if int(Q*2**(ix+N*ix+1-N**2))%2!=int(nv*2**(-2*N))%2 and 0==nv%(2**N)^(~int(Q*2**(N*ix+N-N**2))%(2**N)):
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if not int(Q*2**(j*N+ix+1-N**2))%2!=int(nv*2**(j+1-2*N))%2:
                                iga_j_puhul=False
                                break
                    if iga_j_puhul:
                        Fq+=1
                        #print("Q=",Q,"on vastuolus veeruga",nv,"ix=",ix)
                        break
            #print(Fq,end=";")
            #Fqd.append(Fq)
            sobivaid_ridu+=2**(2**(2*N+1)-Fq)
        #print(Fqd.count(0),Fqd.count(1),Fqd.count(2),Fqd.count(3),Fqd.count(4))
        return sobivaid_ridu
    p = {}  # ajutine

    for Q in range(0,2**(N**2)):
        väistatud_bitte=[0]*(N+1)#ajutine
        ridu_Q_väärtuse_korral=1
        for P1 in range(0,2**(N+1)):
            välistatud_bitte_P1_väärtuse_korral=0#Fq
            s=set()
            for P2 in range(0,2**N):
                #nv
                for ix in range(0,N):
                    iga_j_puhul=False
                    if int(Q*2**(ix+N*ix+1-N**2))%2!=int(P1/2**N)%2 and 0==P2^(~int(Q*(2**N)**(ix+1-N))%(2**N)):#P1[H(ix) in x]!=P1[x in x] and
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if not int(Q*2**(j*N+ix+1-N**2))%2!=int(P1*2**(j+1-N))%2:#Q[H(j) in H(ix)]!=P1[H(j) in x]
                                iga_j_puhul=False
                                break
                    if iga_j_puhul:
                        välistatud_bitte_P1_väärtuse_korral+=1
                        #print("Q=",Q,"on vastuolus veeruga",P1*(2**N)+P2,"ix=",ix)
                        s.add(int(Q*(2**N)**(ix+1-N)))
                        break
            vabu_bitte_P1_väärtuse_korral=2**N-välistatud_bitte_P1_väärtuse_korral
            #print("Q=",Q,"P1=",P1,"korral on vabu bitte",vabu_bitte_P1_väärtuse_korral)
            print("Q=",Q,"P1=",P1,"korral on välistatud bitte",välistatud_bitte_P1_väärtuse_korral)
            väistatud_bitte[välistatud_bitte_P1_väärtuse_korral]+=1#ajutine
            if välistatud_bitte_P1_väärtuse_korral==0:
                ridu_Q_väärtuse_korral*=(2**vabu_bitte_P1_väärtuse_korral)-1
            else:
                ridu_Q_väärtuse_korral*=2**vabu_bitte_P1_väärtuse_korral
        if str(väistatud_bitte) in p:#ajutine
            p[str(väistatud_bitte)]+=1#ajutine
        else:#ajutine
            p[str(väistatud_bitte)]=1#ajutine
        #if väistatud_bitte[0]==2**(N+1)-N and väistatud_bitte[1]==N:#ajutine
        #    print(Q,end=",")
        #for k in range(0,len(väistatud_bitte)):#ajutine
        #    print("Q=",Q,"puhul välistas",väistatud_bitte[k],"P1e",k,"bitti")
        sobivaid_ridu+=ridu_Q_väärtuse_korral
    print("N=",N)#ajutine
    for a in sorted(p.keys(),key=lambda x:p[x]):#ajutine
        print(p[a],"!erineva Q väärtuse puhul:")#ajutine
        for k in range(0,len(väistatud_bitte)):#ajutine
            print("\tvälistas",ast.literal_eval(a)[k],"erinevat P1 väärtust",k,"veergu")#ajutine
    return sobivaid_ridu


#print(ridu2(1), ridu(1))
#print(ridu2(2), ridu(2))
#print(ridu2(3), ridu(3))
#print(ridu(4), veerge(4))


#print(ridu_v1(1))
#print(ridu_v1(2))
#print(ridu_v1(3))
#print(ridu_v1(4))

def ridu_v3(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjleoda miseks dnf formaadis.#K=1#eeldab, et kvantorid ei kehti algmõistete kohta.
    if kvantorid_ei_kehti_alghulkade_kohta:#analüütilised lahendid
        if tohib_teha_kõigi_hulkade_kohta_väiteid:
            return 2**(N**2+2**(2*N+1))
        else:
            return 2**(N**2)*(2**(2**N)-1)**(2**(N+1))#huvitavad algtegurid!
    sobivaid_ridu=0
    #Fqd=[]
    #kui see lihtsustatud saab nii, et enam intereerima ei pea, siis teha sellest generaator.
    if tohib_teha_kõigi_hulkade_kohta_väiteid:
        for Q in range(0,2**(N**2)):
            if Q % 1000 == 0:
                print(Q)
            #print("Q=",bin(Q))
            Fq=0
            for nv in range(0,2**(2*N+1)):
                for ix in range(0,N):
                    iga_j_puhul=False
                    #print(bin(int(Q*2**(N*ix+N-N**2))%(2**N)),bin(nv%(2**N)),"Q=",Q,"nv=",nv,"ix=",ix)
                    if int(Q*2**(ix+N*ix+1-N**2))%2!=int(nv*2**(-2*N))%2 and 0==nv%(2**N)^(~int(Q*2**(N*ix+N-N**2))%(2**N)):
                        iga_j_puhul=True
                        for j in range(0,N):#iga j puhul peab tõene olema.
                            if not int(Q*2**(j*N+ix+1-N**2))%2!=int(nv*2**(j+1-2*N))%2:
                                iga_j_puhul=False
                                break
                    if iga_j_puhul:
                        Fq+=1
                        #print("Q=",Q,"on vastuolus veeruga",nv,"ix=",ix)
                        break
            #print(Fq,end=";")
            #Fqd.append(Fq)
            sobivaid_ridu+=2**(2**(2*N+1)-Fq)
        #print(Fqd.count(0),Fqd.count(1),Fqd.count(2),Fqd.count(3),Fqd.count(4))
        return sobivaid_ridu
    #p = {}  # ajutine
    _2__N=2**N
    _2__Np1=2**(N+1)
    aeg=time.time()
    for Q in range(0,2**(N**2-1)):
        if Q%10000==0:
            print(Q,Q/2**(N**2-1),time.time()-aeg)
            aeg = time.time()
        #väistatud_bitte=[0]*(N+1)#ajutine
        ridu_Q_väärtuse_korral=1
        for P1 in range(0,_2__Np1):
            välistatud_veergusi_P1_ja_Q_korral=set()
            for ix in range(0,N):
                if (not(P1&(1<<ix)))!=(not(P1&(1<<N))):#P1[H(ix) in x]!=P1[x in x] and
                    iga_j_puhul=True
                    for j in range(0,N):#iga j puhul peab tõene olema.
                        if (not(Q&(1<<(j*N+ix))))==(not(P1&(1<<j))):#Q[H(j) in H(ix)]!=P1[H(j) in x]
                            iga_j_puhul=False
                            break
                    if iga_j_puhul:
                        välistatud_veergusi_P1_ja_Q_korral.add(Q//_2__N**ix%_2__N)
                        #print("Q=",Q,"on vastuolus veeruga",P1*(2**N)+P2,"ix=",N-1-ix)
            #print("Q=",Q,"P1=",P1,"korral on vabu bitte",_2__N-len(s))
            #print("Q=",Q,"P1=",P1,"korral on välistatud bitte",len(s))
            #väistatud_bitte[välistatud_bitte_P1_väärtuse_korral]+=1#ajutine
            if len(välistatud_veergusi_P1_ja_Q_korral)==0:
                ridu_Q_väärtuse_korral*=2**_2__N-1
            else:
                ridu_Q_väärtuse_korral*=2**(_2__N-len(välistatud_veergusi_P1_ja_Q_korral))
        #if str(väistatud_bitte) in p:#ajutine
        #    p[str(väistatud_bitte)]+=2#ajutine
        #else:#ajutine
        #    p[str(väistatud_bitte)]=2#ajutine
        #if väistatud_bitte[0]==2**(N+1)-N and väistatud_bitte[1]==N:#ajutine
        #    print(Q,end=",")
        #for k in range(0,len(väistatud_bitte)):#ajutine
        #    print("Q=",Q,"puhul välistas",väistatud_bitte[k],"P1e",k,"bitti")
        sobivaid_ridu+=ridu_Q_väärtuse_korral
    #print("N=",N)#ajutine
    #for a in sorted(p.keys(),key=lambda x:p[x]):#ajutine
    #    print(p[a],"erineva Q väärtuse puhul:")#ajutine
    #    for k in range(0,len(väistatud_bitte)):#ajutine
    #        print("\tvälistas",ast.literal_eval(a)[k],"erinevat P1 väärtust",k,"veergu")#ajutine
    return sobivaid_ridu*2

def ridu_v4(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjleoda miseks dnf formaadis.#K=1#eeldab, et kvantorid ei kehti algmõistete kohta.
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
    p = {}  # ajutine
    _2__N=2**N
    _2__Np1=2**(N+1)
    konstant=(2 ** _2__N) - 1
    konstant2=_2__N*2**(N+1)
    aeg=time.time()
    for Q in range(0,2**(N**2-1)):
        if Q%10000==0:
            print(Q,Q/2**(N**2-1),time.time()-aeg)
            aeg = time.time()
        a=0
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
            if len(välistatud_veerud_P1_ja_Q_korral)==0:
                a+=1
            else:
                b+=len(välistatud_veerud_P1_ja_Q_korral)#b+=Fq
        ab=(a,b)#ajutine
        if ab in p:#ajutine
            p[ab]+=1#ajutine
        else:#ajutine
            p[ab]=1#ajutine
    sobivaid_ridu2=0
    print(p)
    for l in p.keys():
        sobivaid_ridu2+=p[l]*konstant**l[0]*(2**(konstant2-l[0]*_2__N-l[1]))
    print("N=",N)#ajutine
    for l in sorted(p.keys(),key=lambda x:p[x]):#ajutine
        print(p[l]*2,"erineva Q väärtuse puhul: a=",l[0],"b=",l[1],"f=",konstant**l[0]*(2**(konstant2-l[0]*_2__N-l[1])))#ajutine
    return sobivaid_ridu2*2

#print(ridu_v4(1)==108)
#print(ridu_v4(2)==12939750000)
#print(ridu_v4(3)==22614750144745638013702021260937500000000)
#print(ridu_v4(4)==57504776229770941169007545256389841736394692150917543524002427730485332894267940532687727065312682987463395495932747329699841284953161621093750000000000000000)
#print(ridu_v4(5)==34556283262898371093645099183869875566423389568137744895453022122625356133387604707949438614226186417159326907474464038205006178468631108561879313029921057723228155298075946113368807839963526522523031848004262105413688252594807478417249638791195531414955615957022811024209494324264869537391142014818494342036776381097336874580215233971384351214493792797734447459854443760103327596899907701385352204698461218166700448531644768799944040937843949405989305920048801490409137297518208938089771117941360950106749033585130703111215640252037658935139634226202252002613050680828627198934555053710937500000000000000000000000000000000)

#print(ridu_v3(1,kvantorid_ei_kehti_alghulkade_kohta=True)==162)
#print(ridu_v3(2,kvantorid_ei_kehti_alghulkade_kohta=True))
#print(ridu_v3(3,kvantorid_ei_kehti_alghulkade_kohta=True)==163648808609320185659789125078125000000000)
#print(ridu_v3(4,kvantorid_ei_kehti_alghulkade_kohta=True)==878265152102586565157300527505434273010931440172637452061388646005116106279391289007843203658293638072852148354279685278557654731446838378906250000000000000000)

#print(ridu_v4(1)
#print(ridu_v3(2))
#print(ridu_v3(3))
#print(ridu_v3(4))
#print(ridu_v3(5))


def itereeri_üle_Qde_v5_1(Q_min, Q_max, N, _2__N, _2__Np1, out):
    aeg=time.time()
    p={}
    for Q in range(Q_min,Q_max):
        if Q%10000==0:
            print(Q,(Q-Q_min)/(Q_max-Q_min),time.time()-aeg)
            aeg = time.time()
        a=0
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
            #print("Q=",Q,"P1=",(P1+(2**N))%2**(N+1),"korral on vabu bitte",_2__N-len(välistatud_veerud_P1_ja_Q_korral))
            #print("Q=",Q,"P1=",(P1+(2**N))%2**(N+1),"korral on välistatud bitte",len(välistatud_veerud_P1_ja_Q_korral))
            #väistatud_bitte[välistatud_bitte_P1_väärtuse_korral]+=1#ajutine
            if len(välistatud_veerud_P1_ja_Q_korral)==0:
                a+=1
            else:
                b+=len(välistatud_veerud_P1_ja_Q_korral)#b+=Fq
        ab=(a,b)
        if ab in p:
            p[ab]+=1
        else:
            p[ab]=1
    out.put(p)
def itereeri_üle_Qde_v5_2(Q_min, Q_max, N, _2__N, _2__Np1, out):
    aeg=time.time()
    p={}
    for Q in range(Q_min,Q_max):#Q hulga, millesse kuulub järgi indekseerimine võib jõudlust suurendada.
        if Q%40000==0:
            print(Q,(Q-Q_min)/(Q_max-Q_min),time.time()-aeg)
            aeg = time.time()
        b=0
        grupid={}
        #print("Q=", Q)
        for ix in range(0,N):
            ix_i_tingimus1=0
            for j in range(0,N):
                ix_i_tingimus1+=2**j*(not not(Q&(1<<(N*j+ix))))
                ix_i_tingimus2=(not not(Q&(1<<(ix*(N+1)))))
            if (ix_i_tingimus1,ix_i_tingimus2) in grupid:
                grupid[(ix_i_tingimus1,ix_i_tingimus2)].add(ix)
            else:
                grupid[(ix_i_tingimus1,ix_i_tingimus2)]=set({ix})
        for (ix_i_tingimus1,ix_i_tingimus2) in grupid.keys():
            välistatud_P2ed=set()
            for ix in grupid[(ix_i_tingimus1,ix_i_tingimus2)]:
                välistatud_P2ed.add(Q//_2__N**ix%_2__N)
            #print("\tgrupp=", grupid[(ix_i_tingimus1,ix_i_tingimus2)] ,"välistatud P2ed=",välistatud_P2ed)

            b+=len(välistatud_P2ed)#b+=Fq
        ab=(2**(N+1)-len(grupid),b)
        if ab in p:
            p[ab]+=1
        else:
            p[ab]=1
        #print("\tgrupid=", grupid)
        print("Q=",bin(Q)[2:].zfill(N**2),"gruppe on a=",len(grupid),"välistatud veege kokku b=", b)#ajutine
    out.put(p)
def ridu_v5(N, tohib_teha_kõigi_hulkade_kohta_väiteid=False, kvantorid_ei_kehti_alghulkade_kohta=False):#tagastab, et kui palju bitte on vaja seose kirjleoda miseks dnf formaadis.#K=1#eeldab, et kvantorid ei kehti algmõistete kohta.
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
    p = {}  # ajutine
    _2__N=2**N
    _2__Np1=2**(N+1)

    väljundid=multiprocessing.Queue()
    protsesse = multiprocessing.cpu_count()
    protsesse=1#ajutine
    Qsid_protsessis=(2**(N**2-1))//protsesse
    jääk=(2**(N**2-1))%protsesse
    for i in range(0,jääk):
        #print(Qsid_protsessis*i+i,"kuni",Qsid_protsessis*(i+1)+i+1)
        protsess=multiprocessing.Process(target=itereeri_üle_Qde_v5_2, args=(Qsid_protsessis * i + i, Qsid_protsessis * (i + 1) + i + 1, N, _2__N, _2__Np1, väljundid))
        protsess.start()
    for i in range(jääk,protsesse):
        #print(Qsid_protsessis*i+jääk,"kuni",Qsid_protsessis*(i+1)+jääk)
        protsess=multiprocessing.Process(target=itereeri_üle_Qde_v5_2, args=(Qsid_protsessis * i + jääk, Qsid_protsessis * (i + 1) + jääk, N, _2__N, _2__Np1, väljundid))
        protsess.start()
    for i in range(protsesse):
        väljund=väljundid.get()
        for ab_väljund in väljund.keys():
            if ab_väljund in p:
                p[ab_väljund]+=väljund[ab_väljund]
            else:
                p[ab_väljund]=väljund[ab_väljund]

    sobivaid_ridu2=0
    konstant=2**_2__N-1
    konstant2=_2__N*2**(N+1)
    for l in p.keys():
        sobivaid_ridu2+=p[l]*konstant**l[0]*(2**(konstant2-l[0]*_2__N-l[1]))
    print("N=",N)#ajutine
    for l in sorted(p.keys(),key=lambda x:p[x]):#ajutine
        print(p[l]*2,"erineva Q väärtuse puhul: a=",l[0],"b=",l[1],"f=",konstant**l[0]*(2**(konstant2-l[0]*_2__N-l[1])))#ajutine
    return sobivaid_ridu2*2


def itereeri_üle_Qde_v6_1(Q_min, Q_max, N, _2__N,out):
    aeg=time.time()
    p={}
    for Q in range(Q_min,Q_max):#Q hulga, millesse kuulub järgi indekseerimine võib jõudlust suurendada.
        if Q%100000==0:
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
def itereeri_üle_Qde_v6_1(Q_min, Q_max, N, _2__N,out,p2):
    aeg=time.time()
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
        p2[len(grupid)][b]+=1
        #print("Q=",bin(Q),"gruppe on a=",len(grupid),"välistatud veege kokku b=",b)
    out.put(p2)
def f5(N,a,kde_jaotused):#tagastab, et kui palju on Qsid, milles on a i_x'ide gruppi #vajab sisendiks ka järjendit, mis näitab võimalikke hulkade suurusi.
    Qsid=0
    for k_de_jaotus in kde_jaotused:
        n=factorial(2**(N+1))*factorial(N)/factorial(2**(N+1)-a)
        for k in range(1,N+1):
            #print(str(k)+"seid gruppe on",k_de_jaotus[k-1])
            n/=(2**k*factorial(k))**k_de_jaotus[k-1]*factorial(k_de_jaotus[k-1])
        Qsid+=n
    return Qsid
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
        sobivaid_ridu=0
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
    _2__N=2**N

    p2=[]
    for a in range(0,N+1):
        p2.append([])
        for b in range(0,N+1):
            p2[a].append(0)

    väljundid=multiprocessing.Queue()
    protsesse=multiprocessing.cpu_count()
    Qsid_protsessis=(2**(N**2-1))//protsesse
    jääk=(2**(N**2-1))%protsesse
    for i in range(0,jääk):
        #print(Qsid_protsessis*i+i,"kuni",Qsid_protsessis*(i+1)+i+1)
        multiprocessing.Process(target=itereeri_üle_Qde_v6_1, args=(Qsid_protsessis*i+i,Qsid_protsessis*(i+1)+i+1,N, _2__N,väljundid,p2)).start()
    for i in range(jääk,protsesse):
        #print(Qsid_protsessis*i+jääk,"kuni",Qsid_protsessis*(i+1)+jääk)
        multiprocessing.Process(target=itereeri_üle_Qde_v6_1, args=(Qsid_protsessis*i+jääk,Qsid_protsessis*(i+1)+jääk,N, _2__N,väljundid,p2)).start()
    #p2=itereeri_üle_Qde_v6_1(0,Qsid_protsessis+1,N, _2__N,väljundid,p2)
    #print("p2=",p2)
    for i in range(protsesse):
        väljund=väljundid.get()
        for a in range(0,N+1):
            for b in range(0,N+1):
                p2[a][b]+=väljund[a][b]

    konstant=2**_2__N-1
    _2__Np1=2**(N+1)

    sobivaid_ridu2=0
    for a in range(1,N+1):
        for b in range(a,N+1):
            sobivaid_ridu2+=p2[a][b]*konstant**(N-a)*2**((a-1)*_2__N+N-b)
            #sobivaid_ridu2+=f5(a,b)*konstant**(N-a)*2**((a-1)*_2__N+N-b)
    #print("N=",N)#ajutine
    #for l in sorted(p.keys(),key=lambda x:p[x]):#ajutine
    #    print(p[l]*2,"erineva Q väärtuse puhul: on ix'ide gruppe a=",l[0],"gruppides on kokku välistatud b=",l[1],"f=",konstant**(N-l[0])*2**((l[0]-1)*_2__N+N-l[1]))#ajutine
    return sobivaid_ridu2*konstant**(_2__Np1-N)*2**(_2__N-N+1)


print(ridu_v6(5,1,tohib_teha_kõigi_hulkade_kohta_väiteid=True))
print(ridu_v6(1,1)==108)
print(ridu_v6(2,1)==12939750000)
print(ridu_v6(3,1)==22614750144745638013702021260937500000000)
print(ridu_v6(4,1)==57504776229770941169007545256389841736394692150917543524002427730485332894267940532687727065312682987463395495932747329699841284953161621093750000000000000000)
print(ridu_v6(5,1)==34556283262898371093645099183869875566423389568137744895453022122625356133387604707949438614226186417159326907474464038205006178468631108561879313029921057723228155298075946113368807839963526522523031848004262105413688252594807478417249638791195531414955615957022811024209494324264869537391142014818494342036776381097336874580215233971384351214493792797734447459854443760103327596899907701385352204698461218166700448531644768799944040937843949405989305920048801490409137297518208938089771117941360950106749033585130703111215640252037658935139634226202252002613050680828627198934555053710937500000000000000000000000000000000)
#print(ridu_v6(6,1))

def f(N):
    n=1
    for i in range(0,N):
        n*=2**(N+1)-i
    return n//2**(N)

def f2(N, a, kd):#tagastab, et kui palju on Qsid, milles on a i_x'ide gruppi #vajab sisendiks ka järjendit, mis näitab võimalikke hulkade suurusi.
    n=1
    for grupp in range(0,a):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
        #print((2**(N-k[i]+1)-i*2**(-k[i]))/factorial(k[i])*factorial(N))
        n*=(2**(N-kd[grupp]+1)-grupp*2**(-kd[grupp]))/factorial(kd[grupp])
    for k in range(1,N+1):
        n/=factorial(kd.count(k))
    return n*factorial(N)

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
            n*=(2**b-grupp/2)/factorial(kd[grupp])
        for k in range(1,N+1):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
            n/=factorial(kd.count(k))
        return n*factorial(N)
    else:#VALE
        #raise NotImplementedError
        n = 1
        for grupp in range(0,a):
            n*=(2**b-grupp/2)/factorial(kd[grupp])
        for k in range(1,N+1):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis.
            n/=factorial(kd.count(k))
        return n*factorial(N)
def f4(N,a,kde_jaotused):#tagastab, et kui palju on Qsid, milles on a i_x'ide gruppi #vajab sisendiks ka järjendit, mis näitab võimalikke hulkade suurusi.
    print(kde_jaotused)
    Qsid=0
    for k_de_kaoutus in kde_jaotused:
        n=1
        i_x=0
        #print(k_de_kaoutus)
        for j in range(0,N):
            #print(str(j+1)+"seid gruppe on",k_de_kaoutus[j])
            for w in range(k_de_kaoutus[j]):#kui on 2 võrdse suurusega gruppi, siis pole nende järjekord täthtis. see funktsioon arvestab seda.
                #print(((2**(N-(j+1)+1)-i*2**(-(j+1)))/factorial(j+1)))
                n*=((2**(N-(j+1)+1)-i_x*2**(-(j+1)))/factorial(j+1))
                i_x+=1
                #print(n)
            n/=factorial(k_de_kaoutus[j])
        Qsid+=n*factorial(N)
    return Qsid



def moodusta_kde_jaotused(N,a):
    return m(N,a,N,N)
def m(ix_e_jäänud,gruppe_jäänud,max_k,N):
    if ix_e_jäänud<=0 or gruppe_jäänud<=0:
        if ix_e_jäänud==0 and gruppe_jäänud==0:
            return [0]
        return False
    for s_k in range(0,N):
        #print(m(ix_e_jäänud-max_k*s_k,gruppe_jäänud-1,max_k-1,N))
        if m(ix_e_jäänud-max_k*s_k,gruppe_jäänud-1,max_k-1,N):
            return m(ix_e_jäänud-max_k*s_k,gruppe_jäänud-1,max_k-1,N)+[s_k]

#print(moodusta_kde_jaotused(10,5))

#print("N=1",f3(1,1,None,[1]))#2
print("N=1",f3(1,1,1,[1]))#2
#print("N=2",f3(2,1,None,[2]))#2
print("N=2",f3(2,1,1,[2]))#2
#print("N=2",f3(2,2,None,[1,1]))#14
print("N=2",f3(2,2,2,[1,1]))#14
#print("N=3",f3(3,2,None,[1,2]))#90
print("N=3",f3(3,2,2,[2,1]))#42
#print("N=3",f3(3,3,None,[1,1,1]))#420
print("N=3",f3(3,3,3,[1,1,1]))#420
#print("N=4",f3(4,4,None,[1,1,1,1]))#53940
print("N=4",f3(4,4,4,[1,1,1,1]))#53940
#print("N=4",f3(4,2,None,[2,2])+f3(4,2,None,[3,1]))#98+288+48=434
print("N=4",f3(4,2,2,[2,2])+f3(4,2,2,[3,1]))#98
print("N=5",f3(5,3,3,[3,1,1])+f3(5,3,3,[2,2,1]))#10500
print("N=5",f3(5,2,2,[1,4])+f3(5,2,2,[3,2]))#210
print("N=5",f3(5,4,4,[1,1,1,2]))#539400
print("N=5",f3(5,3,5,[1,1,1,1,1]))#4225920#VALE!

#print("N=1",f3(1,1,[1]))#2
#print("N=2",f3(2,1,[0,1]))#2
#print("N=2",f3(2,2,[2,0]))#14
#print("N=3",f3(3,2,[1,1,0]))#90
#print("N=3",f3(3,3,[3,0,0]))#420
#print("N=4",f3(4,4,[4,0,0,0]))#53940
#print("N=5",f3(5,4,[3,1,0,0,0]))#4765320

#print()

#print("N=1",f5(1,1,[[1]])==2)#2
#print("N=2",f5(2,1,[[0,1]])==2)#2
#print("N=2",f5(2,2,[[2,0]]))#14
#print("N=3",f5(3,2,[[1,1,0]]))#90
#print("N=3",f5(3,3,[[3,0,0]]))#420
#print("N=4",f5(4,4,[[4,0,0,0]]))#53940
#print("+N=4",f5(4,2,[[0,2,0,0],[1,0,1,0]]))#98+288+48=434
#print("N=5",f5(5,4,[[3,1,0,0,0]]))#4765320
#print("N=5",f5(5,3,[[2,0,1,0,0],[1,2,0,0,0]]))#195300