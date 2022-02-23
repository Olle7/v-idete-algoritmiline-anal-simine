LÕPPRIDA_ÜHESELT_VALE=üv(LR1_number)

def üv(kontrollitav_plato, kontrollitava_plato_tase=0, eelane=None):
    #kontrollib, et plato p (ükski haru) ei väidaks millegi eksisteerimist, mille eksisteerimist eelane(eelase harud) eitab
    #selleks tuleb kontrollida, et iga eelase jaatatud haru jaoks leiduks mingi kontrollitava plato jatatud haru, nii, et leidub mingi asi mis neid mõlemaid rahuldab.
    for jaatatud_haru_e in eelane:
        for jaatatud_haru_p in kontrollitav_plato:
            #jaatatud_haru_p=sisestakvantor(jaatatud_haru_p,kontrollitav_plato)
            if not on_ühine_rahuldaja(jaatatud_haru_p,jaatatud_haru_e):
                return False

    # kontrollib, et ükski plato p (mingi) haru ei väidaks millegi mitte eksisteerimist, mille eksisteerimist eelane(eelase haru) nõuab.
    # plato p enda kvantor tuleb harude sisse viia.
    # selleks tuleb kontrollida, et iga plato p jaatatud haru jaoks leiduks mingi eelase haru, nii, et leidub mingi asi mis neid mõlemaid rahuldab.
    for jaatatud_haru_p in kontrollitav_plato:
        jaatatud_haru_p = sisestakvantor(jaatatud_haru_p, kontrollitav_plato)
        for jaatatud_haru_e in eelane:
            if not on_ühine_rahuldaja(jaatatud_haru_p,jaatatud_haru_e):
                return False



    for jaatatud_haru in kontrollitav_plato:
        if not üv(jaatatud_haru,kontrollitava_plato_tase+1,kontrollitav_plato):
            return False