def get_veerud(argumendid):
    N=len(argumendid)
    veerud = []
    for i in range(0, N):
        for j in range(0, N):
            veerud.append(argumendid[i] + "∈" + argumendid[j])
    return veerud

veerud=get_veerud("A")
kvantoriga_elementaarväited=DNF(veerud)#iga kvantoriga elementaarväide on üks DNF rida, millele kvantor ümber pannakse
for veerg in kvantoriga_elementaarväited:
    veerg=iga(veerg)
K1_veerud=kvantoriga_elementaarväited+algmoiste_vahlised_väited
lõplikud_read=DNF(K1_veerud)#siin võiks teoreetiliselt ka CNF olla.
lõplikud_read=eemalda_sobimatud(lõplikud_read)#sobimatu on näiteks rida, milles järeldub, et P1(x) ei saa mingit väärtust mómandada.#sobimatu on näiteks väide, millest järeldub mingi algmõistete vaheline seos, mis vastavas veerus on vastandväärtusega.