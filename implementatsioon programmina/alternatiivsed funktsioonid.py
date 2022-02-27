def laiendatud_EKd(self, tipp_sabaga):
    # self on peaks funktsiooni kutsel olema LR
    alluvad_sabaga = self.alluvad_sabaga_eesjärjestuses(eitatute_harudesse_mitte_minna=True,leveleid=1)

    ###
    for i_alluv in range(len(alluvad_sabaga)):
        alluvad_sabaga[i_alluv][-1].predikaadid[Predikaat_väide("n", [])] = str(i_alluv)
    ###

    suhteline_kõrgus = 0
    for eitatud_EK in tipp_sabaga[-1].EKd:
        if not eitatud_EK.märk:
            eitatud_haru_kõrgus = eitatud_EK.suhteline_kõrgus()
            if eitatud_haru_kõrgus > suhteline_kõrgus:
                suhteline_kõrgus = eitatud_haru_kõrgus
    # print("eitatud harude max kõrgus:",suhteline_kõrgus)

    if suhteline_kõrgus == 0:
        return ()
    elif suhteline_kõrgus == 1:  # todo kui see optimeerimis if while seest maha võtta pole ka seda if'i enam vaja.
        for i_tipp in range(1, len(alluvad_sabaga)):
            if alluvad_sabaga[i_tipp][-1].märk:
                laiendatud_haru = Tipp({Predikaat_väide("laiendatud", []): str(i_tipp)}, [], "laiendatud")
                tipp_sabaga[-1].EKd.append(laiendatud_haru)
                yield laiendatud_haru
                kaadrid.append(deepcopy(kaader))
        return

    tipu_max_index = len(alluvad_sabaga) - 1

    kaadrid.append(deepcopy(kaader))
    laiendatud = [tipp_sabaga[-1], Tipp({Predikaat_väide("laiendatud", []): "1"}, [], "laiendatud")]
    laiendatud[-2].EKd.append(laiendatud[-1])
    for i_laiendatud_tipp in range(suhteline_kõrgus - 1):
        laiendatud.append(Tipp({Predikaat_väide("laiendatud", []): "1"}, [], True))
        laiendatud[-2].EKd.append(laiendatud[-1])
    kaadrid.append(deepcopy(kaader))
    # print("muuta: [P1, P1, 'P1']")

    P1 = [1] * suhteline_kõrgus  # algab 1est mitte 0ist, sest LRi pole mõtet muude tippude sisse asendada
    while 1:
        if P1[
            -1] >= tipu_max_index:  # see if ainult optimeerimise pärast, saaks selle eemaldada ja ka viimast numbri loopis koos teiste numbrotega suurendada.#todo: kontrollida, kas see teeb programmi kiiremaks. Vb saaks mingi veelgi efektiivseme variandi, kus gemereeritakse vastava arvu Ifidega baitkoodi ette.
            P1[-1] = 1
            i = suhteline_kõrgus - 2
            while i >= 0:
                if P1[i] == tipu_max_index:
                    P1[i] = 1
                    i -= 1
                else:
                    assert P1[i] < tipu_max_index
                    P1[i] += 1
                    # muutused=P1.copy()#ajutine
                    if i == 0:
                        if not alluvad_sabaga[P1[i]][-1].märk:
                            # print("pOsitsioonil", i, "on eitatud haru nr", P1[i], ":", alluvad_sabaga[P1[i]][-1])
                            continue  # mitte lisada seda laiendatudesse
                        yield laiendatud[1]
                    for i in range(i, suhteline_kõrgus):  # siin loopis uuendatakse laiendatuid.
                        # muutused[i]="P"+str(muutused[i])
                        laiendatud[i + 1] = Tipp({Predikaat_väide("laiendatud", []): str(P1[i])}, [],
                                                 alluvad_sabaga[P1[i]][-1].märk)
                        if i == 0:
                            # print(":::",laiendatud[i].märk)
                            # assert laiendatud[i].märk==True
                            laiendatud[1].märk = "laiendatud"
                        laiendatud[i].EKd.append(laiendatud[i + 1])
                        # print("haru nr:",P1[i_2],alluvad_sabaga[P1[i_2]])
                        if alluvad_sabaga[P1[i]][-1].märk:
                            Tipp._teisenda_predikaatväited(laiendatud, P1, i, alluvad_sabaga)
                            # todo:teisendada siin predikaatväited
                        else:  # kui lisatakse eitatud haru P1'e, siis ei sellest paremale P1'e enam midagi ei tohiks lisada.#todo:kui esimene haru alluvate järjendis on eitatud, siis vist ei lähe siia.
                            Tipp._teisenda_predikaatväited(laiendatud, P1, i,
                                                           alluvad_sabaga)  # teisiti teisendada kui jaatatud haru korral.
                            # todo:eitatute sees asendada tipud samas järjekorras.
                            # print("positsioonil",i,"on eitatud haru nr",P1[i],":",alluvad_sabaga[P1[i]][-1])
                            # print("muuta:", muutused)
                            kaadrid.append(deepcopy(kaader))
                            break
                    else:  # kui polnud eitatuid.
                        # print("muuta:",muutused)
                        break  # SIHTPUNKTI 2
            else:  # kõik numbrid olid maximum(radix) väärtusega.
                yield laiendatud[1]
                for i_alluv in range(len(alluvad_sabaga)):
                    del alluvad_sabaga[i_alluv][-1].predikaadid[Predikaat_väide("n", [])]
                return
        else:  # suurendada ainult viimast numbrit ühe võrra.
            P1[-1] += 1
            laiendatud[-1] = Tipp({Predikaat_väide("laiendatud", []): str(P1[-1])}, [], alluvad_sabaga[P1[-1]][-1].märk)
            laiendatud[-2].EKd.append(laiendatud[-1])
            # muutused=P1.copy()
            # muutused[-1]="p"+str(muutused[-1])
            # todo: teisendada siin predikaatväited

        # print("muuta:",muutused)#SIHTPUNKT2
        kaadrid.append(deepcopy(kaader))
        # print("laiendatud:",laiendatud)


#pdf failis oleva puu pilt jaatatud harusse lisa PVsid panemata:
#assert not LV(E(~A(1,1)&~E(E(~A(3,2)&~A(1,3))&~A(2, 2)&A(2,1)&E(~A(2,3) & A(3,2)&~A(3,3)&E(A(1,4)&A(2,4)&~A(3,4)&~A(4,2)&~A(4,3)&A(4,4))))&E(~A(2,2)&E(~A(3,3)&A(3,1)&A(2,3)&~A(3,2)&E(~A(4,3)&~A(1,4))&E(A(4,4)&~A(4,2)&~A(4,3)&A(3,4)&~A(2,4)&A(1,4)))))).mitte_ÜV()