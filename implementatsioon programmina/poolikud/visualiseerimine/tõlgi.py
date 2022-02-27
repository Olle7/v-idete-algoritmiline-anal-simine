tõlked=[("Tipp","Vertex"),("predikaadid","params"),("eitatud_EKd","type1_branches"),("EKd","type2_branches"),("# MINU MUUTUS","# MY CHANGE")]
if input("Kas eesti keelest inglise keelde?"):
    f = open("visual.py")
    lk = f.read()
    f.close()
    for tõlge in tõlked:
        lk=lk.replace(tõlge[0],tõlge[1])
    tõlgitud=open("visual_eng.py","w")
else:
    f = open("visual_tree.py")
    lk = f.read()
    f.close()
    for tõlge in tõlked:
        lk=lk.replace(tõlge[1],tõlge[0])
    tõlgitud=open("visual_est.py", "w")

tõlgitud.write(lk)
tõlgitud.close()