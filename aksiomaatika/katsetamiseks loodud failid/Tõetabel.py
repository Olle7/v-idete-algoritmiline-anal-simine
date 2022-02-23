def truthtable (n):
    if n < 1:
        yield []
        return
    subtable=truthtable(n-1)
    for row in subtable:
        for v in [False,True]:
            yield row+[v]

class Tõetabel:
    def __init__(self,veerud):
        self.veerud=veerud
    def või_read_stringina(self):
        read=["False"]
        esimene_rida=True
        for rea_booleanid in truthtable(len(self.veerud)):
            if esimene_rida:
                esimene_rida=False
                continue
            rida=""
            esimene_OK=True
            for o in range(0,len(rea_booleanid)):
                if rea_booleanid[o]:
                    if not esimene_OK:
                        rida+="∨"
                    esimene_OK=False
                    rida+=(self.veerud[o])
            read.append(rida)
        return read
    def kvantoriga_või_read_stringina(self):
        read=["False"]
        esimene_rida=True
        for rea_booleanid in truthtable(len(self.veerud)):
            if esimene_rida:
                esimene_rida=False
                continue
            rida="∀_x("
            esimene_OK=True
            for o in range(0,len(rea_booleanid)):
                if rea_booleanid[o]:
                    if not esimene_OK:
                        rida+=")∨∀_x("
                    esimene_OK=False
                    rida+=(self.veerud[o])
            read.append(rida+")")
        return read
    def või_read_funktsioonina(self):
        read=[]
        for rea_booleanid in truthtable(len(self.veerud)):
            rida="("
            esimene_OK=True
            for o in range(0,len(rea_booleanid)):
                if rea_booleanid[o]:
                    if not esimene_OK:
                        rida+=" )or("
                    esimene_OK=False
                    rida+=(self.veerud[o])
            print(rida)
            read.append(compile(rida+")"))
        return read
    def ja_read_stringina(self):
        read=[]
        for rea_booleanid in truthtable(len(self.veerud)):
            rida=""
            for o in range(0, len(rea_booleanid)):
                if not rea_booleanid[o]:
                    rida+="¬"
                rida+=(str(self.veerud[o])+"∧")
            read.append(rida[:-1])
        return read
    def ja_read_funktsioonina(self):
        pass

def moodusta_kuulumised_stringina(hulgad1, hulgad2):
    kuulumised=[]
    for hulk1 in hulgad1:
        for hulk2 in hulgad2:
            kuulumised.append("("+hulk1+" in "+hulk2+")")
    return kuulumised


P1=Tõetabel(moodusta_kuulumised_stringina(["A","x"],["x"])).ja_read_stringina()#"OMADUS"
#print(P1)
P2=Tõetabel(moodusta_kuulumised_stringina(["x"],["A"])).ja_read_stringina()#"JÄRELDUS"
#print(P2)

võimalikud_kvatnotri_sisud=Tõetabel(P2).või_read_stringina()[1:]#on omavahel sõltuvad.
print(võimalikud_kvatnotri_sisud)

võimalikud_kvatnotrite_kombinatsioonid=Tõetabel(võimalikud_kvatnotri_sisud).kvantoriga_või_read_stringina()[1:]
print(len(võimalikud_kvatnotrite_kombinatsioonid))
print(võimalikud_kvatnotrite_kombinatsioonid)