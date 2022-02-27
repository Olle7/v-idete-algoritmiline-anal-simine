

LÕPPRIDA_ÜHESELT_VALE=f(LR1_number)

#Üheselt tõseid platosid(eksistentsiaalkvanotoreid) ei ole.
def eemalda_sisemised_kvantorid(plato,mitu_taset_eemaldada):
    uus_plato=0
    identsete_grupi_suurus=veerge(K-mitu_taset_eemaldada)#L
    for i in range(veerge(k)/veerge(K-m)):
        if saa_bitid(plato,i*identsete_grupi_suurus+log(H(k),2),(i+1)*identsete_grupi_suurus+log(H(k),2)):#True kui ei võrdu nulliga
            uus_plato+=2**i
    return uus_plato

def saa_bitid(arv,kõrgem_indeks,madalam_indeks):#least significant bitt on indeksiga 0.
    return arv//2**madalam_indeks%2**kõrgem_indeks

def veerge(k):
    if k==K:
        return 0
    return 2**(k+1)*H(k+1)

def f(kontrollitav_plato, kontrollitava_plato_tase=0, eelased=[]):
    """
    :param kontrollitav_plato:
    :param kontrollitava_plato_tase:
    :param eelased: väited, mille abil kontrollitakse, et kas kvantor on üheselt vale või mitte. Eelastest on eemaldatud nii palju sisemisi kvantoreid, et kontrollitava plato ja eelaste Ksügavus oleks võrdne
    :return: True kui vastav plato (kvantor ilma võimaliku ees oleva eituseta) ei ole üheselt vale, False kui kvantor(ilma võimaliku ees oleva eituseta) on üheselt vale. Teisisõnu Kontrollib, et kas antud kvantori kvanteeritav saab eksisteerida või mitte."""
    for eelase_tase in range(len(eelased)):
        eelane=eelased[eelase_tase]
        if eemalda_sisemised_kvantorid(eelane,kontrollitava_plato_tase-eelase_tase)!=eemalda_kõrgemad_konstandid(kontrollitav_plato, kontrollitava_plato_tase-eelase_tase):#vahest oleks efektiivsem biti kaupa kontrollida, sest siis ei peaks kõiki bitte välja arvutama kui juba üks esimestest ei klapi.
            return False

    #eelased.append(kontrollitav_plato)
    #for eelase_tase in range(len(eelased)):
    #    eelased[eelase_tase] = eemalda_sisemised_kvantorid(eelased[eelase_tase],eelase_tase)

    for haru,haru_märk in kontrollitav_plato:
        if haru_märk and not f(haru,kontrollitava_plato_tase+1, eelased):#kui haru on jaatatud ja on üheselt vale #Kõigile eelaste argumendiks andmine võib olla ebaefektiivne, sest see on kõigis funktsiooni ktutsetes sama ja seda ei muudeta funktsioonis. Alati argumendiks andmine tähendab pythonis selle alati kopeerimist.
            return False
    return True



#see, et mis numbritega lõppread on valed sõltub ainult Kst,Nist, ja seosefunktsioonidest.
#Kui k, N ja seosefunktsioonid on teada saab üheselt valede lõppridade numbrid leida ja need vahele jätta.