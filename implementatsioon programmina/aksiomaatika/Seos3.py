class Seos():
    """
        Kõigis formaatides salvestutud seosed on selle alamklassid.
    """
    def __str__(self):
        raise NotImplementedError
    def get_K(self):
        raise NotImplementedError
    def __and__(self,other):
        raise NotImplementedError
    def __or__(self,other):
        raise NotImplementedError
    def __xor__(self,other):
        raise NotImplementedError




class lihtne_DNF(Seos):#panna see laiendama klassi sympy class Seos(sympy):
    """
        Selle klassi eesmärk on panna hulkade vaheline seos kirja arvutile loetaval kujul. Alghulkadele vastava tähenduse valimisel võib seoset kasutada ka näiteks naturaalarvude,reaalarvude ja aritmeetiliste tehete defineerimiseks.
    """
    def __init__(self, seos_muus_formaadis, K=None, N=None,alghulgad=None,alghulkade_kirjeldused=None):
        konvertia[type(seos_muus_formaadis)][lihtne_DNF](seos_muus_formaadis)
    def __str__(self):
        pass
    def get_seos_ridadena(self):
        pass
    def get_veerud(self):
        pass
    def get_read(self):
        pass
    def get_rida(self,rea_nr):
        pass
    def get_veerg(self,veeru_nr):
        pass
    def get_K(self):
        return self.K
    def __and__(self,other):
        pass
    def __or__(self,other):
        pass
    def __xor__(self,other):
        pass





def str_to_lihtne_DNF(teksti_kujul):
    elementaarseosed=leia_elementaarseosed(parsitud)
    lõppveerg=0
    for LR in range(max_LR):
        lõppveerg+=on_kookõlas(seos,LR)*2**LR
    return lõppveerg



def str_to_eemaldatud_ridadega_DNF(teksti_kujul):
    elementaarseosed = leia_elementaarseosed(parsitud)
    taseme_funktsioonide_väärtuste_arv=leia_tasemefunktsioonide_väärtuste_arv(parsitud)

    lõppveerg = 0
    LR=0
    for i in range(max_LR)
        if ei_ole_üheselt_vale(LR):
            LR+=1
        lõppveerg+=on_kookõlas(seos,LR)*ei_ole_üheselt_vale(LR)*2**LR
    return lõppveerg


konvertia={str:{lihtne_DNF:str_to_lihtne_DNF}}