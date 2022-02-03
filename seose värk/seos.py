#selle faili omanik on Olger Männik. Kõik peale visualiseerimise osa sellest on minu poolt kirjutatud. Tahan säilitada kõik võimalikud õigused selle faili sisule.

#TODO: special field in vertexes to indicate if the vertex must be under or above a special horisontal line. May assume that branches o of vertixes that are over line are also always over line.
#TODO: crossing out type2 edges should cover type1 edges.
import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import deque
class Tree_Visualize:
    def __init__(self,frames):
        self.f=plt.figure()
        self.f.add_subplot(111)

        self.window = tk.Tk()
        self.window.title("frame: 0")
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.window.bind("<Right>", lambda x:self.swich_frame(1))
        self.window.bind("<Left>", lambda x:self.swich_frame(-1))
        self.canvas = FigureCanvasTkAgg(self.f, master=self.window)
        self.canvas.get_tk_widget().pack(side='top', fill='both',expand=1)  # `side='top', fill='both', expand=1` will resize plot when you resize window
        toolbar=NavigationToolbar2Tk(self.canvas, self.window)
        toolbar.update()
        self.frames=frames
        self.i_frame=0
        self.root_vertex = self.frames[0]
        self.generate_tree()
        self.window.mainloop()
    def swich_frame(self, n_frames_to_swich):
        if self.i_frame+n_frames_to_swich<len(self.frames):
            self.i_frame += n_frames_to_swich
            self.window.title("frame:" + str(self.i_frame))

            # for item in self.canvas.get_tk_widget().find_all():
            #    self.canvas.get_tk_widget().delete(item)
            self.f.clear()

            self.root_vertex=self.frames[self.i_frame]
            self.generate_tree()
        else:
            print("Nii palju kaadreid pole. Kuvatakse kaadrit:", self.i_frame)
    def quit(self,event):
        self.window.destroy()
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
    @staticmethod
    def leia_max_pikkusega_rida(text):
        jupid=text.split("\n")
        max_pikkus=0
        for jupp in jupid:
            if len(jupp)>max_pikkus:
                max_pikkus=len(jupp)
        return max_pikkus
    def generate_tree(self):
        G=nx.Graph()
        dq=deque([self.root_vertex])
        #type2_edge_labels={}
        sildid_küljel={}
        to_end_of_lv=1
        colors=[]
        while dq:
            vert=dq.pop()
            to_end_of_lv-=1
            if (isinstance(vert.predikaadid, dict)):
                sildid_küljel[vert] = [False, False]
                if to_end_of_lv == 0:
                    sildid_küljel[vert][0]=True
                    to_end_of_lv = len(dq) + 1
                if to_end_of_lv == 1:
                    sildid_küljel[vert][1]=True
            else:
                add_param_names=[False,False]
                if to_end_of_lv==0:
                    add_param_names[0]=True
                    to_end_of_lv=len(dq)+1
                if to_end_of_lv==1:
                    add_param_names[1]=True
                sildid_küljel[vert]=Tree_Visualize.get_predikaadid(vert,add_param_names=add_param_names)
            if isinstance(vert,LV):
                for i_EK in range(len(vert.LRid)):
                    G.add_edge(vert, vert.LRid[i_EK])
                    colors.append((1,1,0))#kollane
                    dq.appendleft(vert.LRid[i_EK])
            else:
                for i_EK in range(len(vert.EKd)):
                    G.add_edge(vert, vert.EKd[i_EK])
                    dq.appendleft(vert.EKd[i_EK])
                    if vert.EKd[i_EK].märk=="laiendatud":
                        colors.append((0,0,1))#sinine
                    elif vert.EKd[i_EK].märk:
                        colors.append((0,1,0))#roheline #TODO: kaaluda mustaks teha
                    else:
                        colors.append((1,0,0))#punane
                        #type2_edge_labels[id(vert),id(vert.EKd[i_EK])]='x'
        if G.number_of_nodes()!=0:
            pos = Tree_Visualize.hierarchy_pos(G, self.root_vertex)
            labeldict=Tree_Visualize.fill_the_gaps_of_the_param_tree(G, self.root_vertex, sildid_küljel)

            for node, (x, y) in pos.items():
                if sildid_küljel[node][0]:
                    x-=0.0025*Tree_Visualize.leia_max_pikkusega_rida(labeldict[node])#kuna see nihe on suhtelise osana ekraani suurusest, aga texti font o pikslites, siis erinevatel ekraanidel võib erinevat niihet vaja olla.
                if sildid_küljel[node][1]:
                    x+=0.0025*Tree_Visualize.leia_max_pikkusega_rida(labeldict[node])
                pos[node]=(x,-y)
            #üks võimalus, et kõik ära mahuks on vähendada fondi suurust.
            nx.draw(G,pos=pos,font_weight="bold",font_size=7,node_size=0,node_color='white',labels=labeldict,with_labels=True,edge_color=colors)
            #nx.draw_networkx_edge_labels(G, flipped_pos, edge_labels=type2_edge_labels, font_color='red')
        else:
            G.add_node("FALSE")
            nx.draw(G,node_color='yellow',labels={"FALSE":"FALSE\nLV:+:LV"},with_labels=True)
        plt.subplots_adjust(top=1.05,right=1.05,left=-0.05,bottom=-0.05,hspace=0,wspace=0)
        self.canvas.draw()
        #self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)
    @staticmethod
    def fill_the_gaps_of_the_param_tree(G, root, sildid_küljel):
        labeldict={}
        level = 0
        while True:
            level_nodes = []
            level_predikaadid = []
            nodes = set(nx.ego_graph(G, root, radius=level))
            nodes -= set(nx.ego_graph(G, root, radius=level - 1))
            nodes = list(nodes)
            if len(nodes) == 0:
                break
            else:
                for node in nodes:
                    if (isinstance(node.predikaadid, dict)):
                        level_nodes.append(node)
                        level_predikaadid.extend(node.predikaadid.keys())
                level_predikaadid = list(set(level_predikaadid))
                """
                final_level_predikaadid = []
                for param in level_predikaadid:
                    match = False
                    for param1 in final_level_predikaadid:
                        try:
                            if param == param1:
                                match = True
                        except Exception as e:
                            print(e)
                    if match == False:
                        final_level_predikaadid.append(param)
                level_predikaadid=final_level_predikaadid
                """#kui on mitu võrdset asja level_predikaadid'es, siis viskab 1 neist välja.
                try:
                    level_predikaadid.sort(reverse=True, key=Tipp.predikaatväidete_sorteerimise_võti)
                except Exception as e:
                    print(e)
                node_count = 0
                for node in nodes:
                    if (isinstance(node.predikaadid, dict)):
                        labels = []
                        for key_name in level_predikaadid:
                            if key_name in node.predikaadid.keys():
                                if node.predikaadid[key_name] == False:  # MINU MUUTUS
                                    labels.append("-")
                                elif node.predikaadid[key_name] == True:  # MINU MUUTUS
                                    labels.append("+")
                                else:  # MINU MUUTUS
                                    labels.append(node.predikaadid[key_name])
                            else:
                                labels.append(" ")
                            if sildid_küljel[node][0]:
                                labels[-1]=str(key_name)+": "+labels[-1]
                            if sildid_küljel[node][1]:
                                labels[-1]+=" :"+str(key_name)
                        labeldict[node] = '\n'.join(labels)
                        node_count += 1
                max_predikaadid = 0
                for node in nodes:
                    if (labeldict[node].count('\n') > max_predikaadid):
                        max_predikaadid = labeldict[node].count('\n')
                for node in nodes:
                    labeldict[node] = '\n' * int(max_predikaadid - labeldict[node].count('\n')) + labeldict[node]
            level = level + 1
        return labeldict
    @staticmethod
    def hierarchy_pos(G, root=None, width=1, vert_gap=0.2, vert_loc=0, xcenter=0.5):
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))

        def _hierarchy_pos(G, root, width=0.5, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)
            if len(children)!=0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2

                for child in children:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                         vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root)
            return pos

        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    @staticmethod
    def get_predikaadid(vertex):
        final_str = ""
        v = vertex.predikaadid[::-1]
        for i in v:
            if i == False:
                final_str += "-"
            elif i == True:
                final_str += "+"
            else:
                final_str += i
            final_str += "\n"
        return final_str[:-1]

from sympy import Symbol, to_dnf, Or, And, Not
from sympy.logic.boolalg import Boolean
from copy import deepcopy
#TODO:Et performany parendada võib Sympyst ainult need asjad oma projekti kopeerida, mida kasutan ja liigsed väljad kustutada.

#TODO:kui ainult predikaadid, NOR ja U on pole sympit enam vb. vaja. Ülejäänud seose enda sees defineeritud.
class Predikaat_väide(Symbol):#võib symbol asemel pärineda Atomist või Booleanist.
    def __new__(self, nimi, argumendid=[]):
        predikaat_väide=Symbol.__new__(self, nimi+"("+','.join([str(i) for i in argumendid])+")")
        predikaat_väide.argumendid=tuple(argumendid)
        predikaat_väide.nimi=nimi
        return predikaat_väide
    def __lt__(self, other):
        if isinstance(other,Predikaat_väide):
            if self.argumendid!=other.argumendid:
                return self.argumendid<other.argumendid
            else:
                return self.nimi<other.nimi
        elif isinstance(other,str):
            return False
        else:
            return super(Predikaat_väide, self).__lt__(self,other)
    def __hash__(self):
        return hash((self.argumendid,self.nimi))
    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        result = cls.__new__(cls,deepcopy(self.nimi),deepcopy(self.argumendid)) # Create a new instance of the object based on extracted class
        return result
class Predikaat:
    def __init__(self,nimi):
        self.nimi=nimi
    def __call__(self, *args, **kwargs):
        return Predikaat_väide(self.nimi,args)
class E(Symbol):#TODO: võiks ka funktsioon olla, mis kohe lihtsustatud vormi tagastab.
    def __new__(self,sisu):
        E=Symbol.__new__(self,"∃("+str(sisu)+")")
        E.sisu=sisu
        return E
def U(sisu):
    return (~E(~sisu))


class Tipp:
    def __init__(self,predikaadid,EKd,märk):
        self.predikaadid=predikaadid#predikaadid #oluline, et kõik erinevad predikaatväited siin oleksid erinevate hash'idega!
        self.EKd=EKd#eksistentsiaalsus_kvantorid
        self.EKd.sort()
        self.märk=märk#Kas jaatatud või eitatud
    def __str__(self):
        sees=[]
        for pv in sorted(self.predikaadid.items(), key=Tipp.predikaatväidete_sorteerimise_võti):
            if type(pv[1])==bool:
                sees.append((not pv[1])*"¬"+str(pv[0]))
            else:
                sees.append("("+str(pv[0])+"="+pv[1]+")")
        for EK in self.EKd:
            sees.append(str(EK))
        if self.märk=="LR":
            if not sees:
                return "TRUE"
            else:
                return " & ".join(sees)
        return ((not self.märk)*"¬")+"∃("+" & ".join(sees)+")"
    def __repr__(self):
        return self.__str__()
    def suhteline_kõrgus(self):#TODO:saaab leida koos teega alluvateni.
        dq=[self]
        lv=0
        max_lv=0
        while dq:
            vert = dq.pop()
            if vert == True:
                lv += 1
                if lv>max_lv:
                    max_lv=lv
                continue
            if vert == False:
                lv -= 1
                continue
            dq.append(False)
            for branch in vert.EKd:
                dq.append(branch)
            dq.append(True)
        return max_lv
    def alluvad_sabaga_eesjärjestuses(self,eitustest_mitte_läbi_minna=False,eitatute_harudesse_mitte_minna=False,laiendatuid_mitte_võtta=True,leveleid=None,tipp_ise_ka=False):
        if leveleid==None:
            leveleid=float("inf")
        dq=[self]
        tee=[None]
        alluvad_eesjärjestus=[]
        while dq:
            tipp=dq.pop()
            if tipp==True:
                tee.append(None)
                continue
            if tipp==False:
                tee.pop()
                continue
            tee[-1]=tipp
            alluvad_eesjärjestus.append(tee.copy())
            dq.append(False)
            if (not eitatute_harudesse_mitte_minna or tipp.märk) and len(tee)<=leveleid:
                for EK in tipp.EKd[::-1]:
                    if (not eitustest_mitte_läbi_minna or EK.märk) and (not laiendatuid_mitte_võtta or EK.märk!="laiendatud"):
                        dq.append(EK)
            dq.append(True)
        if not tipp_ise_ka:
            alluvad_eesjärjestus.pop(0)
        return alluvad_eesjärjestus
    def täida_eitatud_asendus(self,algne_eitatud_tipp,leveleid,i,P1,alluvad_sabaga):
        assert leveleid>=0
        if leveleid==0:
            return
        dq=[algne_eitatud_tipp[-1]]
        algne_tee=[None]
        uus_tee=[Tipp({},[],[]),self]
        while dq:
            tipp=dq.pop()
            if tipp==True:
                algne_tee.append(None)
                uus_tee.append(None)
                continue
            if tipp==False:
                algne_tee.pop()
                uus_tee.pop()
                continue
            algne_tee[-1]=tipp
            if len(algne_tee)!=1:  # kui ei lähe esimest korda while-tsüklisse.
                uus_tee[-1]=Tipp({},[],None)
            uus_tee[-2].EKd.append(uus_tee[-1])
            uus_tee[-1].märk=algne_tee[-1].märk

            ####
            if len(algne_tee)!=1:
                for predikaatväide,predikaatväite_väärtus in algne_tee[-1].predikaadid.items():
                    #print("pv, tipus, mis on P1es madalaml või sama kõrgel ja puus kõrgemal või sama kõrgel kui alluvad_sabaga[P1[i1]].")#itereerib üle kõigi predikaatväidete, mis on P1es madalamal või sama kõrgel ja puus kõrgemal või sama kõrgel.
                    uute_predikaatväidete_argumendid=[[]]
                    if isinstance(predikaatväide,Predikaat_väide):
                        for a in predikaatväide.argumendid:
                            if a>=len(algne_eitatud_tipp)-1:#kui a tipp on puus peale algset eitatud tippu
                                indexid_P1es=[a+2+i-len(algne_eitatud_tipp)]
                            else:#kui a tipp on puus enne algset eitatud tippu
                                #print("P1:",P1)
                                #print("tipp enne eitatud haru: a=",a," ; argumendi tipp=",algne_eitatud_tipp[a])
                                argumendi_tipp=algne_eitatud_tipp[a]#See tipp mille kvanteeritav argumendiks on.
                                #print("a:",a,"; a-tipp:",argumendi_tipp)
                                indexid_P1es=[]#Näitab, et mis indeksitel(see tipp või P1es mitu korda olla) argumendi(kvanteeritava) a tipp P1es on.
                                for i3 in range(i+1):
                                    #print("i3:",i3,"; alluvad_sabaga[P1[i3]][-1]:",alluvad_sabaga[P1[i3]][-1])
                                    if alluvad_sabaga[P1[i3]][-1]==argumendi_tipp:
                                        #Mis indeksil selle argumendi(kvanteeritava) kvantor(tipp) P1es on.
                                        indexid_P1es.append(i3+1)
                            #print("indexid_P1es:",indexid_P1es)
                            vana_uute_predikaatväidete_argumendid=uute_predikaatväidete_argumendid.copy()#todo:optimeerimiseks saab kopeerimise eemaldada.
                            uute_predikaatväidete_argumendid=[]
                            for v in vana_uute_predikaatväidete_argumendid:
                                for index_P1es in indexid_P1es:#TODO: lihtne lihtsustus
                                    uute_predikaatväidete_argumendid.append(v+[index_P1es])
                            if not indexid_P1es:
                                #print("predikaatväidet argumentidega",uute_predikaatväidete_argumendid,"ei lisatud tippu",uus_tee[-1],", sest 1 selle argumendi tipp ei olnud asenduse harus. originaal:",predikaatväide)
                                break
                        else:
                            for uue_predikaatväite_argumendid in uute_predikaatväidete_argumendid:
                                uus_tee[-1].predikaadid[Predikaat_väide(predikaatväide.nimi,uue_predikaatväite_argumendid)]=predikaatväite_väärtus#+"l:"+str(P1[i1])+"i:"+str(P1[i2])
                                #print("täitmises: tipule",uus_tee[-1],"lisati predikaatväide",Predikaat_väide(predikaatväide.nimi,uue_predikaatväite_argumendid))
                                #print("algne väide:",predikaatväide)
            ####
            dq.append(False)
            if len(uus_tee)<=leveleid+1:
                for EK in tipp.EKd[::-1]:
                    dq.append(EK)
            dq.append(True)
    @staticmethod
    def _teisenda_predikaatväited(laiendatud, P1, alluvad_sabaga, tipu_kuhu_asendatakse_k):
        for i2 in range(len(P1)):
            #print("eelneja P1es:",P1[i2])
            if alluvad_sabaga[P1[-1]][-1] in alluvad_sabaga[P1[i2]]:#alluvad[P1[i1]] ja alluvad[P1[i2]] on samal joonel puus. alluvad[P1[i2]] kõrgemal.
                #print(P1[i2],"(",i2,")","on madalamal P1es ja kõrgemal puus kui ",P1[-1],"(",-1,") ; P1=",P1)
                for predikaatväide,predikaatväite_väärtus in alluvad_sabaga[P1[i2]][-1].predikaadid.items():
                    #print("pv tipus, mis on P1es madalaml või sama kõrgel ja puus kõrgemal või sama kõrgel kui alluvad_sabaga[P1[-1]]:",predikaatväide)#itereerib üle kõigi predikaatväidete, mis on P1es madalamal või sama kõrgel ja puus kõrgemal või sama kõrgel.
                    uute_predikaatväidete_argumendid=[[]]
                    if isinstance(predikaatväide,Predikaat_väide):
                        for a in predikaatväide.argumendid:
                            argumendi_tipp=alluvad_sabaga[P1[i2]][a]#See tipp mille kvanteeritav argumendiks on.
                            indexid_puus=[]#Näitab, et mis indeksitel(see tipp või P1es mitu korda olla) argumendi(kvanteeritava) a tipp P1es on.
                            for i3 in range(len(P1)):#todo: või i2'eni itereerida?
                                if alluvad_sabaga[P1[i3]][-1]==argumendi_tipp:
                                    #Mis indeksil selle argumendi(kvanteeritava) kvantor(tipp) P1es on.
                                    indexid_puus.append(i3+1)
                            vana_uute_predikaatväidete_argumendid=uute_predikaatväidete_argumendid.copy()#todo:optimeerimiseks saab kopeerimise eemaldada.
                            uute_predikaatväidete_argumendid=[]
                            for v in vana_uute_predikaatväidete_argumendid:
                                for index_P1es in indexid_puus:
                                    uute_predikaatväidete_argumendid.append(v+[index_P1es])
                            if not indexid_puus:
                                #print("predikaatväidet argumentidega",uute_predikaatväidete_argumendid,"ei lisatud tippu",P1[i1],"(",i1+1,"), sest 1 selle argumendi tipp ei olnud asenduse harus. originaal:",pv)
                                break
                        else:
                            for uue_predikaatväite_argumendid in uute_predikaatväidete_argumendid:
                                if len(P1) in uue_predikaatväite_argumendid:
                                    laiendatud[len(P1)-tipu_kuhu_asendatakse_k].predikaadid[Predikaat_väide(predikaatväide.nimi, uue_predikaatväite_argumendid)]=predikaatväite_väärtus#+"l:"+str(P1[i1])+"i:"+str(P1[i2])
                                    #print("tipule",P1[-1],"(",len(P1),")","lisada predikaatväide",Predikaat_väide(predikaatväide.nimi,uue_predikaatväite_argumendid))
                                    #print("algne väide:",predikaatväide,"algne tipp:",P1[-1],"(",i2+1,")\n")
                                    #print("P1:",len(P1))
                                #else:
                                    #print("predikaatväidet argumentidega",uue_predikaatväite_argumendid,"ei lisatud tippu",P1[-1],"(", len(P1), "), sest seal polnud vastava tippu kvanteeritavat.\n")
    def laiendatud_EKd(self, tipp_kuhu_asendatakse_sabaga):#FAILIS "alternatiivsed funktsioonid.py" on teistsugune ja vb. efektiivsem implementatsioon sellest funktsioonist.
        #self peaks funktsiooni kutsel olema LR
        alluvad_sabaga=self.alluvad_sabaga_eesjärjestuses(eitatute_harudesse_mitte_minna=True)
        ###
        for i_alluv in range(len(alluvad_sabaga)):
            alluvad_sabaga[i_alluv][-1].predikaadid["n"]=str(i_alluv)
        ###

        suhteline_kõrgus=0
        for eitatud_EK in tipp_kuhu_asendatakse_sabaga[-1].EKd:
            if not eitatud_EK.märk:
                eitatud_haru_kõrgus=eitatud_EK.suhteline_kõrgus()
                if eitatud_haru_kõrgus>suhteline_kõrgus:
                    suhteline_kõrgus=eitatud_haru_kõrgus
        #print("eitatud harude max kõrgus:",suhteline_kõrgus)
        if suhteline_kõrgus==0:
            return ()

        tipu_max_index=len(alluvad_sabaga)-1
        kaadrid.append(deepcopy(kaader))
        P1=[]
        for s in tipp_kuhu_asendatakse_sabaga:
            for i_alluv in range(len(alluvad_sabaga)):
                if s==alluvad_sabaga[i_alluv][-1]:
                    P1.append(i_alluv)
        tipu_kuhu_asendatakse_k=len(P1)

        for i in range(len(alluvad_sabaga)):
            if alluvad_sabaga[i][-1].märk:
                break
        P1.append(i)
        P1+=[0]*(suhteline_kõrgus-1)
        laiendatud=[tipp_kuhu_asendatakse_sabaga[-1]]+[None]*suhteline_kõrgus
        kaadrid.append(deepcopy(kaader))
        #print("muuta: [P1, P1, 'P1']")
        G=True
        while 1:
            i=len(P1)-1
            while i>=tipu_kuhu_asendatakse_k:
                if P1[i]==tipu_max_index:
                    P1[i]=0
                    i-=1
                else:
                    assert P1[i]<tipu_max_index
                    if not G:
                        P1[i]+=1
                    #muutused=P1.copy()#ajutine
                    if i==tipu_kuhu_asendatakse_k:
                        #print("i==tipu_kuhu_asendatakse_k")
                        #print("alluvad_sabaga[P1[i]][-1]:",alluvad_sabaga[P1[i]][-1])
                        if not alluvad_sabaga[P1[i]][-1].märk:#eitatud harusid otse sisse ei asendata.
                            #print("positsioonil",i,"on eitatud haru nr",P1[i],":",alluvad_sabaga[P1[i]][-1])
                            continue#mitte lisada seda laiendatudesse
                        yield laiendatud[1]
                    if G:
                        G=False
                        i=tipu_kuhu_asendatakse_k
                    for i in range(i,tipu_kuhu_asendatakse_k+suhteline_kõrgus):#siin loopis uuendatakse laiendatuid.
                        #muutused[i]="P"+str(muutused[i])
                        laiendatud[i-tipu_kuhu_asendatakse_k+1]=Tipp({"P1["+str(i+1)+"]":str(P1[i])},[],alluvad_sabaga[P1[i]][-1].märk)
                        if i==tipu_kuhu_asendatakse_k:
                            #assert laiendatud[i-tipu_kuhu_asendatakse_k].märk==True or laiendatud[i-tipu_kuhu_asendatakse_k].märk=="LR"#kahtlane, et märk ka "LR" võib olla.
                            laiendatud[1].märk="laiendatud"
                        #print("muuta:", muutused)
                        laiendatud[i-tipu_kuhu_asendatakse_k].EKd.append(laiendatud[i-tipu_kuhu_asendatakse_k+1])
                        Tipp._teisenda_predikaatväited(laiendatud,P1[:i+1], alluvad_sabaga,tipu_kuhu_asendatakse_k)
                        if not alluvad_sabaga[P1[i]][-1].märk:#kui lisatakse eitatud haru P1'e, siis ei sellest paremale P1'e enam midagi ei tohiks lisada.#todo:kui esimene haru alluvate järjendis on eitatud, siis vist ei lähe siia.
                            #print("positsioonil",i,"on eitatud haru nr",P1[i],":",alluvad_sabaga[P1[i]][-1])
                            laiendatud[i-tipu_kuhu_asendatakse_k+1].täida_eitatud_asendus(alluvad_sabaga[P1[i]],suhteline_kõrgus-i-1+tipu_kuhu_asendatakse_k,i,P1,alluvad_sabaga)
                            kaadrid.append(deepcopy(kaader))
                            break
                    else:
                        #print("polnud eitatuid:")
                        #print("muuta:",muutused)
                        break#SIHTPUNKTI 2
            else:
                #print("Lõpp, sest madalaim lubatud P1 ideks sai nullitud.")
                yield laiendatud[1]
                for i_alluv in range(len(alluvad_sabaga)):
                    del alluvad_sabaga[i_alluv][-1].predikaadid["n"]
                return
            #print("muuta:",muutused)#SIHTPUNKT2
            kaadrid.append(deepcopy(kaader))
    @staticmethod
    def täpsem_kui(EK1,EK2):
        for EK2_pv in EK2.predikaadid:
            for EK1_pv in EK1.predikaadid:
                if EK1_pv==EK2_pv:
                    break
            else:
                return False
        for EK2_jaatatud_EK in EK2.EKd:
            if EK2_jaatatud_EK.märk:
                for EK1_pv in EK1.laiendatud_EKd():
                    if Tipp.täpsem_kui(EK1_pv,EK2_pv):
                        break
                else:
                    return False
        for EK2_eitatud_EK in EK2.eitatud_EKd:
            if not EK2_eitatud_EK.märk:
                for EK1_pv in EK1.eitatud_EKd:
                    if EK2_pv>>EK1_pv:
                        break
                else:
                    return False
        return True
    @staticmethod
    def sisud_kooskõlas(tipp1,tipp2):
        pass
    def mitte_ÜV(self):
        #TODO:Saab puu koostamisega kokku panna ja kontrollida ÜVd juba enne täielikku parssimist.
        #TODO:Need harud võib eemaldada, mille olemasolu saab järeldada teisi mingi järjekorras valides.
        #TODO:saab asendada ka eitatud kvantoreid. Kahe P1 elemendi vaheline seos ei säili, kui esimesest(P1'es väiksema indeksiga) teise minemiseks tuleb tagurpidi läbida eitatud haru.
        #todo:Juba enne LRe puustruktuur. nii et kui mingist harust on laiendatud EKde lisamise abil mingi uus saadud, siis uus saab selle haru haruks.
        for tipp_sabaga in self.alluvad_sabaga_eesjärjestuses(eitustest_mitte_läbi_minna=True,tipp_ise_ka=True):
            tipp_ÜV=False
            #todo:Kui laiendatud_EKsse tuleb eitatud kvanto poolikult(kõrgemad oksad puudu), siis see tugvendab eitatud_EKd, ja muudab algoritmi valeks.
            for l_EK in self.laiendatud_EKd(tipp_sabaga):
                for eitatud_EK in self.EKd:
                    if not eitatud_EK.märk:
                        if Tipp.täpsem_kui(l_EK, eitatud_EK):  # l_EK täpsem või võrdne kui eitatud_EK(ja kooskõlas).
                            # self.EKd.pop(0)
                            print("laiendatud haru",l_EK,"on täpsem kui eitatud haru",eitatud_EK)
                            tipp_ÜV = True
                            break  # LR on ÜV
                        if Tipp.sisud_kooskõlas(eitatud_EK,l_EK):#kui pole kindel, et asjal, mille eksisteerimist l_EK väidab ei pea selleks, et selle eksisteerimine eitatud l_EK poolt keelatud poleks, olema omadusi, mida l_EK sisus pole kirjeldatud ja selleks ei pea sellega seoses uusi asju eksisteerima või mitte eksisteerima.
                            print("laiendatud haru", l_EK, "ja eitatud haru", eitatud_EK,"sisud on kooskõlas.")
                            #sellest, mis l_EK sees otseselt kirjas on ei piisa, et järeldada, et l_EK poolt kirjeldatu eksisteerimine pole eitatud l_EK poolt keelatud.
                            #eitatud_EK täpsem kui l_EK või eitatud_EK on täpsuselt võrreldamatu EKga.
                            # kui l_EK kirjeldatud:
                            #    asjal peavad olema mingid predikaat väited,
                            #    asjaga seoses peavad muud asjad eksisteerima või
                            #    muud asjad ei tohi selle asjaga mingil viisil seotud olles eksisteerida
                            # et l_EK kirjeldatud asja eksiteerimine poleks eitatud l_EK poolt eitatud
                            # ja seda pole l_EK sees otseselt kirjas.
                            pass#Luua uusi LRe, EKsse on lisatud vastasmärgiga eitatud_EK harusid, et l_EK ja eitatud_EK sisud ei oleks kooskõlas.
    #                    else:
    #                        pass#sellest, mis l_EK sees otseselt kirjas on piisab, et järeldada, et see pole eitatud l_EK poolt keelatud.
                if tipp_ÜV:
                    break
            if tipp_ÜV:
                break
        #Tree_Visualize(kaadrid)
        #kaadrid.append(deepcopy(LV))
        return [Tipp({"t":"T"},[],True)]#True
    def __lt__(self,other):#todo: mõelda, et mille järgi sorteerida.
        return (self.märk, sorted(self.predikaadid.items(), key=Tipp.predikaatväidete_sorteerimise_võti), self.EKd) < (other.märk, sorted(other.predikaadid.items(), key=Tipp.predikaatväidete_sorteerimise_võti), other.EKd)
    @staticmethod
    def predikaatväidete_sorteerimise_võti(x):
        if isinstance(x, tuple):
            pv=x[0]
            väärtus=x[1]
        else:
            pv=x
            väärtus=None
        if not isinstance(pv, Predikaat_väide):
            return ((-float("inf"),),pv,väärtus)
        else:
            return (pv.argumendid,pv.nimi,väärtus)
#    def __eq__(self, other):
#        return self.märk==other.märk and self.predikaadid==other.predikaadid and self.EKd==other.EKd
class LV:
    def __init__(self,seos):
        if isinstance(seos,Boolean):
            self.predikaadid={"LV":True}
            self.LRid=[]
            for LR in LV.koosta_puu(seos):
                assert LR.märk==True
                LR.märk="LR"
                self.LRid.append(LR)
            self.LRid.sort()
        else:
            self.LRid=seos
            self.predikaadid={"P":"p"}
            #raise NotImplementedError
    def __str__(self):
        sees=[]
        if not self.LRid:
            return "FALSE"
        for ek in self.LRid:
            sees.append(str(ek))
        return " | ".join(sees)
    def __repr__(self):
        return self.__str__()
    def LRid_sabaga_eesjärjestuses(self,leveleid=None):
        if leveleid==None:
            leveleid=float("inf")
        dq=[self]
        tee=[None]
        alluvad_eesjärjestus=[]
        while dq:
            tipp=dq.pop()
            if tipp==True:
                tee.append(None)
                continue
            if tipp==False:
                tee.pop()
                continue
            tee[-1]=tipp
            #print("tee:",tee," ; type(tee[-1]):",type(tee[-1]))
            if isinstance(tee[-1],Tipp):
                alluvad_eesjärjestus.append(tee.copy())
            else:
                dq.append(False)
                if len(tee)<=leveleid:
                    for EK in tipp.LRid[::-1]:
                        dq.append(EK)
                dq.append(True)
        return alluvad_eesjärjestus
    def mitte_ÜV(self):
        #TODO:kui laiendada Expr klassi siis saab selle ehk klassimeetodiks teha. Et seda saaks otse Sympy avaldistele või klassi E objektidele rakendada.
        #TODO:Saab puu koostamisega kokku panna ja kontrollida ÜVd juba enne täielikku parssimist.
        global kaadrid,kaader
        kaader=self
        kaadrid=[deepcopy(self)]

        ######ajutine
        #for LR in self.LRid:
        #    LR.mitte_ÜV()
        #Tree_Visualize(kaadrid)
        #input("######")
        ######

        ajutine=0
        while self.LRid and ajutine<3:
            ajutine+=1
            LRid_sabaga=self.LRid_sabaga_eesjärjestuses()
            #print(len(LRid_sabaga))
            for i_LR in range(len(LRid_sabaga)):
                juurde_tekitatud_harud=LRid_sabaga[i_LR][-1].mitte_ÜV()
                if juurde_tekitatud_harud==True:
                    Tree_Visualize(kaadrid)
                    return True
                elif juurde_tekitatud_harud==[]:
                    LRid_sabaga[i_LR][-2].LRid.remove(LRid_sabaga[i_LR][-1])
                else:
                    LRid_sabaga[i_LR][-2].LRid[LRid_sabaga[i_LR][-2].LRid.index(LRid_sabaga[i_LR][-1])]=LV(juurde_tekitatud_harud)
        Tree_Visualize(kaadrid)
        return False
    def __bool__(self):
        if not self.mitte_ÜV():
            return False
        elif not (~self).mitte_ÜV():
            return True
        else:
            raise Exception("Unknown if true or false.")
    @staticmethod
    def _asenduste_valikud(võimalikke_väärtusi):
        num=[]
        for i in võimalikke_väärtusi:
            if i==None:
                num.append(-1)
            else:
                num.append(0)
        while True:
            yield num
            for i in range(0,len(võimalikke_väärtusi)):
                if num[i]==võimalikke_väärtusi[i]:
                    num[i]=0
                elif võimalikke_väärtusi[i]!=None:
                    num[i]+=1
                    break
            else:
                return
    @staticmethod
    def _jaota_osadesse(boolean_väide):
        boolean_väide=to_dnf(boolean_väide.simplify(),True)
        if type(boolean_väide)==Or:
            boolean_väide=boolean_väide.args
        elif boolean_väide==True:
            yield ({},[],[])
            return
        elif boolean_väide==False:
            return
        else:
            boolean_väide=[boolean_väide]
        #print("järjend omavahel ORiga eraldatud olnud osadest:",boolean_väide)
        for dnf_element in boolean_väide:
            if type(dnf_element)==And:
                sisu=dnf_element.make_args(dnf_element)
            else:
                sisu=[dnf_element]
            predikaadid={}
            eitatud_Ed=[]
            Ed=[]
            #print("järjend omavahel ANDiga eraldatud olnud osadest:",sisu)
            for jaatuse_element in sisu:
                tüüp=type(jaatuse_element)
                if tüüp==E:
                    Ed.append(jaatuse_element)
                elif tüüp==Not:
                    if type(jaatuse_element._args[0])==E:
                        eitatud_Ed.append(jaatuse_element._args[0])
                    else:
                        assert type(jaatuse_element._args[0])==Predikaat_väide
                        predikaadid[jaatuse_element._args[0]]=False
                else:
                    assert tüüp==Predikaat_väide
                    predikaadid[jaatuse_element]=True
            yield (predikaadid,eitatud_Ed,Ed)
    @staticmethod
    def koosta_puu(seos, k=0):
        sisemised_kvantorid=[]
        sisemiste_kvantorite_võitatud_vormid=[]
        for sisemine_kvantor in seos.atoms():
            if type(sisemine_kvantor)==E:
                sisemised_kvantorid.append(sisemine_kvantor)
                vv=LV.koosta_puu(sisemine_kvantor.sisu,k+1)
                if not vv:#todo: kas on vaja
                    vv=[False]
                sisemiste_kvantorite_võitatud_vormid.append(vv)
        #print(seos, " :sisemiste_kvantorite_võitatud_vormid:", sisemiste_kvantorite_võitatud_vormid)
        #print("type:", t2ype(seos), "; plato:", seos, ";")
        võitatud_vormid=[]
        for sisemise_võituse_elemendi_p_osa,sisemise_võituse_elemendi_u_osa,sisemise_võituse_elemendi_e_osa in LV._jaota_osadesse(seos):
            #print("osa:",sisemise_võituse_elemendi_p_osa,sisemise_võituse_elemendi_u_osa,sisemise_võituse_elemendi_e_osa)
            for i_sisemine_kvantor in range(len(sisemise_võituse_elemendi_u_osa)):#teeb asendused U-osas.
                #TODO:PEAB need üheks kvantoriks ühendama, et saaks teada, kas midagi saab kõrgemalt alla poole tuua.
                eitatud_ek=sisemise_võituse_elemendi_u_osa.pop(0)
                #print("    eitatud kvantor:",eitatud_ek)
                for variant in sisemiste_kvantorite_võitatud_vormid[sisemised_kvantorid.index(eitatud_ek)]:
                    sisemise_võituse_elemendi_u_osa.append(variant)
                    sisemise_võituse_elemendi_u_osa[-1].märk=False
                    #print("      u-ossa lisada:",variant," ; TÜÜP=",type(variant))
            asenduste_valik=[None]*len(sisemised_kvantorid)
            for sisemine_kvantor in sisemise_võituse_elemendi_e_osa:#määrab, et kui palju variante kui mitmenda kvantori asendamiseks E-osas on.
                i=sisemised_kvantorid.index(sisemine_kvantor)
                asenduste_valik[i]=len(sisemiste_kvantorite_võitatud_vormid[i])-1
            for asenduste_valik in LV._asenduste_valikud(asenduste_valik):
                välimise_võituse_elemendi_e_osa=[]
                for i in range(len(asenduste_valik)):#TODO: asendada ainult muutunud indeksitega(asenduste valikus) kvantorid.
                    if asenduste_valik[i]!=-1:#kõik ja ainult U'd asendatakse mingi Plato'e või predikaatide vahelise booleanseosega.
                        #print("    asendada:",sisemised_kvantorid[i],":",sisemiste_kvantorite_võitatud_vormid[i][asenduste_valik[i]])
                        välimise_võituse_elemendi_e_osa.append(deepcopy(sisemiste_kvantorite_võitatud_vormid[i][asenduste_valik[i]]))
                võitatud_vormid.append(Tipp(sisemise_võituse_elemendi_p_osa,välimise_võituse_elemendi_e_osa+sisemise_võituse_elemendi_u_osa,True))
        #print("  võitatud vormid:",võitatud_vormid)
        return võitatud_vormid


if __name__=="__main__":
    A=Predikaat("A")
    B=Predikaat("B")
    C=Predikaat("C")
    #print(koosta_puu(E(A(1) & A(1, 1) & E(A(1, 2) & E(A(2, 3) & A(3, 1))))))

    M=Predikaat("x1’le meeldib x2")
    on_mari = Predikaat("x1 on mari")

    on_null=Predikaat("on_null")
    võrdne=Predikaat("võrdne")
    PEANO=E(on_null(1))&\
          ~E(~võrdne(1,1))&\
          ~E(E(E(~((võrdne(1,2)&võrdne(2,3))>>võrdne(3,1)))))
    #peano_puu=LV(PEANO).mitte_ÜV()
    #print("Peano tulem:", peano_puu)
    #print("\n#####\n")

    class Test:
        def __init__(self,sisend,puu_str,bool="?"):
            self.sisend=sisend
            self.puu_str=puu_str
            self.bool=bool
#        def test(self):
#            return self.puu_str_test and self.bool_test
        def puu_str_test(self):
            lv=LV(self.sisend)
            arvutatud_puu_str=str(lv)
            if arvutatud_puu_str!=self.puu_str:
                print("Puu valesti koostatud.")
                print("SISEND :",self.sisend)
                print("TULEMUS:",arvutatud_puu_str)
                print("OODATUD:",self.puu_str)
                print()
                return False
            return True
        def bool_test(self):
            lv = LV(self.sisend)
            try:
                arvutatud_bool=bool(lv)
            except Exception as e:
                if e.args!="Unknown if true or false.":
                    raise e
                arvutatud_bool=None
            if arvutatud_bool!=self.bool and self.bool!="?":
                print("ÜVsus või ÜTsus valesti määratud")
                print("SISEND :", self.sisend)
                print("TULEMUS:", arvutatud_bool)
                print("OODATUD:", self.bool)
                print()
                return(False)
            return(True)
    tests=[
        #jaatatud haru E(A(1,1)) sisse tuleb lisada jaatatud märgiga E(A(1,2)&A(2,2)), et eitatud ja laiendatud haru sisud vastuollu läheks.
        Test(~E(A(1,1)&~E(A(1,2)&A(2,2)))&E(A(1,1))&E(B(1,1)),"¬∃(A(1,1) & ¬∃(A(1,2) & A(2,2))) & ∃(A(1,1))",None),

        #jaatatud haru E(A(1,1) sisse tuleb lisada ~B(1,1) , E(A(1,2)&A(2,2)) või E(~B(2,1)&B(2,2)), et eitatud ja laiendatud haru sisud vastuollu läheks.
        Test(~E(A(1,1)&B(1,1)&~E(A(1,2)&A(2,2))&E(~B(2,1)&B(2,2)))&E(A(1,1)),"¬∃(A(1,1) & ¬∃(A(1,2) & A(2,2))) & ∃(A(1,1))",None),

        #vist O'ga ÜV kontroll annab vale tulemuse (tegelt ÜV).
        Test(E(~A(1,1)&E(A(1,2)&~A(2,1)&~A(2,2)&E(~A(1,3)&A(2,3)&~A(3,1)&~A(3,2)&~A(3,3))&E(~A(1,3)&A(2,3)&~A(3,1)&~A(3,2)&A(3,3))))&~E(~A(1,1)&E(~A(1,2)&A(2,1)&~A(2,2)&E(A(1,3)&~A(2,3)&~A(3,1)&~A(3,2)&~A(3,3))&E(A(1,3)&~A(2,3)&~A(3,1)&~A(3, 2) &A(3,3)))),"¬∃(¬A(1,1) & ∃(¬A(1,2) & A(2,1) & ¬A(2,2) & ∃(A(1,3) & ¬A(2,3) & ¬A(3,1) & ¬A(3,2) & ¬A(3,3)) & ∃(A(1,3) & ¬A(2,3) & ¬A(3,1) & ¬A(3,2) & A(3,3)))) & ∃(¬A(1,1) & ∃(A(1,2) & ¬A(2,1) & ¬A(2,2) & ∃(¬A(1,3) & A(2,3) & ¬A(3,1) & ¬A(3,2) & ¬A(3,3)) & ∃(¬A(1,3) & A(2,3) & ¬A(3,1) & ¬A(3,2) & A(3,3))))",False),

        #ÜV: P1=[1,3]
        #kuna A(1,1) on eitatud harus määramata, siis jaatatus harus predikaatväited x1'ega pole siin olulised.
        Test(~E(~A(1,1)&E(~A(2,2)&A(1,2)&A(2,1)))&~E(A(1,1)&E(A(2,2)&A(1,2)&~A(2,1)))&~E(~A(1,1)&E(~A(2,2)&~A(1,2)&~A(2,1)))&  E(E(~A(2,2)&A(1,2)&A(2,1))&E(A(2,2)&~A(1,2)&E(A(3,3)&~A(3,2)&~A(2,3)&A(1,3)&A(3,1))&E(~A(3,3)&A(3,2)&A(2,3)&~A(1,3)&~A(3,1)&E(A(4,4)&A(2,4)&~A(4,2)&~A(1,4)&A(4,1))))),"¬∃(¬A(1,1) & ∃(¬A(1,2) & ¬A(2,1) & ¬A(2,2))) & ¬∃(¬A(1,1) & ∃(A(1,2) & A(2,1) & ¬A(2,2))) & ¬∃(A(1,1) & ∃(A(1,2) & ¬A(2,1) & A(2,2))) & ∃(∃(¬A(1,2) & A(2,2) & ∃(¬A(1,3) & A(2,3) & ¬A(3,1) & A(3,2) & ¬A(3,3) & ∃(¬A(1,4) & A(2,4) & A(4,1) & ¬A(4,2) & A(4,4))) & ∃(A(1,3) & ¬A(2,3) & A(3,1) & ¬A(3,2) & A(3,3))) & ∃(A(1,2) & A(2,1) & ¬A(2,2)))",False),

        # [kõigil, kes Marile meeldivad,[ei ole kedagi kes Marile meeldiks, aga temale mitte ja kellele meeldiks Mari] või [ei ole kedagi, kes nii talle kui Marile meeldiks] või [on keegi, kes neile meeldib ja kes iseendale meeldib]] ja
        # ja leidub keegi, kes meeldib marile, nii, et eksisteerib [keegi, kes meeldib nii marile kui talle] ja [keegi, kes meeldib marile, kellele mari meeldib ja kelle ei meeldi talle] ja ei leidu kedagi, kes nii iseendale kui ka talle ta meeldiks
        # või [on keegi(x_1) kes endale meeldib, aga [kellel pole kedagi kes nii talle kui iseendale meeldiks ja kellele meeldiks tema(x_1)]]
        Test(E(on_mari(1) & ~E(M(1, 2) & E(M(1, 3) & ~M(2, 3) & M(3, 1)) & E(M(1, 3) & M(2, 3)) & ~E(M(2, 3) & M(3, 3))))&E(E(on_mari(2)&M(2,1)&E(M(1,3)&M(2,3))&E(M(2,3)&M(3,2)&~M(1,3)))&~E(M(2,1)&M(2,2)))| E(M(1,1)&~E(M(1,2)&M(2,2)&M(2,1))),"∃(¬∃(x1’le meeldib x2(2,1) & x1’le meeldib x2(2,2)) & ∃(x1 on mari(2) & x1’le meeldib x2(2,1) & ∃(¬x1’le meeldib x2(1,3) & x1’le meeldib x2(2,3) & x1’le meeldib x2(3,2)) & ∃(x1’le meeldib x2(1,3) & x1’le meeldib x2(2,3)))) & ∃(x1 on mari(1) & ¬∃(x1’le meeldib x2(1,2) & ¬∃(x1’le meeldib x2(2,3) & x1’le meeldib x2(3,3)) & ∃(x1’le meeldib x2(1,3) & ¬x1’le meeldib x2(2,3) & x1’le meeldib x2(3,1)) & ∃(x1’le meeldib x2(1,3) & x1’le meeldib x2(2,3)))) | ∃(x1’le meeldib x2(1,1) & ¬∃(x1’le meeldib x2(1,2) & x1’le meeldib x2(2,1) & x1’le meeldib x2(2,2)))",None),

        #sellest on failis pilt:
        Test(E(~A(1,1)&~E(E(~A(3,2)&~A(1,3))&~A(2, 2)&A(2,1)&E(~A(2,3) & A(3,2)&~A(3,3)&E(A(1,4)&A(2,4)&~A(3,4)&~A(4,2)&~A(4,3)&A(4,4))))&E(~A(2,2)&A(2,1)&E(~A(3,3)&A(3,1)&A(2,3)&~A(3,2)&E(~A(4,3)&~A(1,4)&A(2,4))&E(A(4,4)&~A(4,2)&~A(2,4)&~A(4,3)&A(3,4)&~A(2,4)&A(1,4)&~A(4,1))))),"∃(¬A(1,1) & ¬∃(A(2,1) & ¬A(2,2) & ∃(¬A(1,3) & ¬A(3,2)) & ∃(¬A(2,3) & A(3,2) & ¬A(3,3) & ∃(A(1,4) & A(2,4) & ¬A(3,4) & ¬A(4,2) & ¬A(4,3) & A(4,4)))) & ∃(A(2,1) & ¬A(2,2) & ∃(A(2,3) & A(3,1) & ¬A(3,2) & ¬A(3,3) & ∃(¬A(1,4) & A(2,4) & ¬A(4,3)) & ∃(A(1,4) & ¬A(2,4) & A(3,4) & ¬A(4,1) & ¬A(4,2) & ¬A(4,3) & A(4,4)))))",False),

        #pilt sellest failis:
        Test(E(~A(1, 1) & E(A(1, 2) & ~A(2, 1) & ~A(2, 2))) & ~E(E(~A(2,1))&~A(1, 1) & E(~A(1, 2) & A(2, 1) & ~A(2, 2)&E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3)))),"¬∃(¬A(1,1) & ∃(¬A(1,2) & A(2,1) & ¬A(2,2) & ∃(A(1,3) & ¬A(2,3) & ¬A(3,1) & ¬A(3,2) & A(3,3))) & ∃(¬A(2,1))) & ∃(¬A(1,1) & ∃(A(1,2) & ¬A(2,1) & ¬A(2,2)))",False),

        Test(~E(A(1)&B(1)&C(1)),"¬∃(A(1) & B(1) & C(1))",None),
        Test((E(~A(1,1)&B(1))|E(C(1)&E(A(1,2)|A(2,1)&E(E(E(A(5,1)|A(5,3))))))),"∃(B(1) & ¬A(1,1)) | ∃(C(1) & ∃(A(1,2))) | ∃(C(1) & ∃(A(2,1) & ∃(∃(∃(A(5,1)))))) | ∃(C(1) & ∃(A(2,1) & ∃(∃(∃(A(5,3))))))"),
        Test(~E(A(1)&A(2)),"¬∃(A(1) & A(2))",None),
        Test(~E(A(1,1) | B(1) & C(1)) & E(A(1,1) & A(1) & E(A(2,1))),"¬∃(B(1) & C(1)) & ¬∃(A(1,1)) & ∃(A(1) & A(1,1) & ∃(A(2,1)))",False),
        Test(E(A(1,1))&E(A(1,1)>>E(A(1,2)&~E(A(1,3)|A(3,1)&~E(A(1,1)&A(2,1))))),"∃(∃(A(1,2) & ¬∃(A(1,3)) & ¬∃(A(3,1) & ¬∃(A(1,1) & A(2,1))))) & ∃(A(1,1)) | ∃(¬A(1,1)) & ∃(A(1,1))"),
        Test(E(E(E(võrdne(1,2)&on_null(1)&on_null(2)))),"∃(∃(∃(on_null(1) & võrdne(1,2) & on_null(2))))",None),
        Test(~E(B(1)<<A(1)),"¬∃(¬A(1)) & ¬∃(B(1))",None),
        Test(E(A(1)|B(1))&E(A(1)|B(1))&E(A(1)|B(1)),"∃(A(1)) | ∃(B(1))",None),

        Test(E(A(1))&~E(A(1)),"FALSE",False),
        Test(~(E(A(1))&~E(A(1))),"TRUE",True),
        Test(E(A(1)&B(1))&~E(A(1)),"¬∃(A(1)) & ∃(A(1) & B(1))",False),
        Test(E(A(1))&~E(A(1)&B(1)),"¬∃(A(1) & B(1)) & ∃(A(1))",None),
        Test(E(A(1,1)&~E(~(A(2,2)&~A(1,2)&A(2,1)))),"∃(A(1,1) & ¬∃(A(1,2)) & ¬∃(¬A(2,1)) & ¬∃(¬A(2,2)))",False),
        Test(E(A(1,1)&~E(~(A(2,2)&A(1,2)&~A(2,1)))),"∃(A(1,1) & ¬∃(¬A(1,2)) & ¬∃(A(2,1)) & ¬∃(¬A(2,2)))",False),
        Test(E(A(1, 1)&~E(~(A(2, 2)>>(~A(1, 2)&A(2, 1))))),"∃(A(1,1) & ¬∃(A(1,2) & A(2,2)) & ¬∃(¬A(2,1) & A(2,2)))",False),
        Test(E(E(E(E(A(1,2,3,4)|~B(1,3,4,2)|C(1))))),"∃(∃(∃(∃(C(1))))) | ∃(∃(∃(∃(A(1,2,3,4))))) | ∃(∃(∃(∃(¬B(1,3,4,2)))))",None),


        Test(E(~A(1))&E(A(1)),"∃(¬A(1)) & ∃(A(1))",None),

        #etuatud kvantor tühi:
        Test(E(A(1,1)&E(A(2,1)&~A(1,2)&~E(A(3,2)&A(3,1)))),"∃(A(1,1) & ∃(¬A(1,2) & A(2,1) & ¬∃(A(3,1) & A(3,2))))",None),

        Test(E(A(1))&E(A(1)|B(1)),"∃(A(1)) & ∃(A(1)) | ∃(A(1)) & ∃(B(1))",None),
        ]

    for test in tests:
        test.puu_str_test()
        test.bool_test()

    #BUG:
    #assert (LV(U(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))&E(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))).mitte_ÜV())#tegelt ÜV?

    #BUG:
    #LV(~E(E(E(A(1,2,3)))&A(1,1,1)|E(~A(2,2,1)|~A(1,1,2)&~E(A(3,3,3)&A(3,2,1)))|E(A(2,2,2)&~A(2,1,2)&A(2,2,1))&E(A(2,1,2)&A(2,2,1)|~A(2,2,2)&A(2,1,1)|E(A(3,2,3)&A(3,1,3))))).mitte_ÜV()

    #BUG:
    #LV(~E(E(E(A(1,2,3)))&A(1,1,1)|E(~A(1,1,2)&~E(A(3,3,3)&A(3,2,1)))|E(A(2,2,2)&~A(2,1,2)&A(2,2,1))&E(A(2,1,2)&A(2,2,1)))).mitte_ÜV()