#TODO: special field in vertexes to indicate if the vertex must be under or above a special horisontal line. May assume that branches o of vertixes that are over line are also always over line.
#TODO: crossing out type2 edges should cover type1 edges.
import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import deque
import gc
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
    def generate_tree(self):
        G=nx.Graph()
        dq=deque([self.root_vertex])
        #type2_edge_labels={}
        labeldict={}
        to_end_of_lv=1
        colors=[]
        while dq:
            vert=dq.pop()
            to_end_of_lv-=1
            if (isinstance(vert.predikaadid, dict)):
                labeldict[id(vert)] = [False, False]
                if to_end_of_lv == 0:
                    labeldict[id(vert)][0]=True
                    to_end_of_lv = len(dq) + 1
                if to_end_of_lv == 1:
                    labeldict[id(vert)][1]=True
            else:
                add_param_names=[False,False]
                if to_end_of_lv==0:
                    add_param_names[0]=True
                    to_end_of_lv=len(dq)+1
                if to_end_of_lv==1:
                    add_param_names[1]=True
                labeldict[id(vert)]=Tree_Visualize.get_predikaadid(vert,add_param_names=add_param_names)
            if isinstance(vert,LV):
                for i_EK in range(len(vert.LRid)):
                    G.add_edge(id(vert), id(vert.LRid[i_EK]))
                    colors.append((1,1,0))#kollane
                    dq.appendleft(vert.LRid[i_EK])
            else:
                for i_EK in range(len(vert.EKd)):
                    G.add_edge(id(vert), id(vert.EKd[i_EK]))
                    dq.appendleft(vert.EKd[i_EK])
                    if vert.EKd[i_EK].m??rk=="laiendatud":
                        colors.append((0,0,1))#sinine
                    elif vert.EKd[i_EK].m??rk:
                        colors.append((0,1,0))#roheline #TODO: kaaluda mustaks teha
                    else:
                        colors.append((1,0,0))#punane
                        #type2_edge_labels[id(vert),id(vert.EKd[i_EK])]='x'
        pos = Tree_Visualize.hierarchy_pos(G, id(self.root_vertex))
        #print("type(pos.keys()[0]):",type(list(pos.keys())[0]))
        #print("type(labeldict.keys()[0]):", type(list(labeldict.keys())[0]))
        #flipped_pos={node: (x, -y) for (node, (x, y)) in pos.items()}
        flipped_pos={}
        for node, (x, y) in pos.items():
            if node in labeldict:
                #print("labeldict[node]:",labeldict[node])
                if labeldict[node][0]:
                    x-=0.01#kuna see nihe on suhtelise osana ekraani suurusest, aga texti font o pikslites, siis erinevatel ekraanidel v??ib erinevat niihet vaja olla.
                if labeldict[node][1]:
                    x+=0.01
            #print("x,y:",x,y)
            flipped_pos[node]=(x,-y)
        Tree_Visualize.fill_the_gaps_of_the_param_tree(G, self.root_vertex, labeldict)
        #??ks v??imalus, et k??ik ??ra mahuks on v??hendada fondi suurust.
        nx.draw(G,pos=flipped_pos,font_weight="bold",font_size=7,node_size=0,node_color='white',labels=labeldict,with_labels=True,edge_color=colors)
        #nx.draw_networkx_edge_labels(G, flipped_pos, edge_labels=type2_edge_labels, font_color='red')
        plt.subplots_adjust(top=1.05,right=1.05,left=-0.05,bottom=-0.05,hspace=0,wspace=0)
        self.canvas.draw()
        #self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)
    @staticmethod
    def fill_the_gaps_of_the_param_tree(G, root, labeldict):
        level = 0
        while True:
            level_nodes = []
            level_predikaadid = []
            nodes = set(nx.ego_graph(G, id(root), radius=level))
            nodes -= set(nx.ego_graph(G, id(root), radius=level - 1))
            nodes = list(nodes)
            if len(nodes) == 0:
                break
            else:
                for node in nodes:
                    node_obj = Tree_Visualize.objects_by_id(node)
                    if (isinstance(node_obj.predikaadid, dict)):
                        level_nodes.append(node_obj)
                        level_predikaadid.extend(node_obj.predikaadid.keys())
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
                """#kui on mitu v??rdset asja level_predikaadid'es, siis viskab 1 neist v??lja.
                def v??ti(esimene):
                    if isinstance(esimene,str):
                        return (0,esimene)
                    else:
                        return (1,esimene)
                try:
                    level_predikaadid.sort(reverse=True,key=v??ti)
                except Exception as e:
                    print(e)
                node_count = 0
                for node in nodes:
                    node_obj = Tree_Visualize.objects_by_id(node)
                    if (isinstance(node_obj.predikaadid, dict)):
                        labels = []
                        for key_name in level_predikaadid:
                            if key_name in node_obj.predikaadid.keys():
                                if node_obj.predikaadid[key_name] == False:  # MINU MUUTUS
                                    labels.append("-")
                                elif node_obj.predikaadid[key_name] == True:  # MINU MUUTUS
                                    labels.append("+")
                                else:  # MINU MUUTUS
                                    labels.append(node_obj.predikaadid[key_name])
                            else:
                                labels.append(" ")
                            if labeldict[id(node_obj)][0]:
                                labels[-1]=str(key_name)+": "+labels[-1]
                            if labeldict[id(node_obj)][1]:
                                labels[-1]+=" :"+str(key_name)
                        labeldict[id(node_obj)] = '\n'.join(labels)
                        node_count += 1
                max_predikaadid = 0
                for node in nodes:
                    if (labeldict[node].count('\n') > max_predikaadid):
                        max_predikaadid = labeldict[node].count('\n')
                for node in nodes:
                    labeldict[node] = '\n' * int(max_predikaadid - labeldict[node].count('\n')) + labeldict[node]
            level = level + 1
    @staticmethod
    def objects_by_id(id_):
        for obj in gc.get_objects():
            if id(obj) == id_:
                return obj
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
    def get_predikaadid(vertex):  # My CHANGED FUNCTION
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
#TODO:Et performany parendada v??ib Sympyst ainult need asjad oma projekti kopeerida, mida kasutan ja liigsed v??ljad kustutada.

#TODO:kui ainult predikaadid, NOR ja U on pole sympit enam vb. vaja. ??lej????nud seose enda sees defineeritud.
class Predikaat_v??ide(Symbol):#v??ib symbol asemel p??rineda Atomist v??i Booleanist.
    def __new__(self, nimi, argumendid=[]):
        predikaat_v??ide=Symbol.__new__(self, nimi+"("+','.join([str(i) for i in argumendid])+")")
        predikaat_v??ide.argumendid=tuple(argumendid)
        predikaat_v??ide.nimi=nimi
        return predikaat_v??ide
    def __lt__(self, other):
        if isinstance(other,Predikaat_v??ide):
            if self.argumendid!=other.argumendid:
                return self.argumendid<other.argumendid
            else:
                return self.nimi<other.nimi
        elif isinstance(other,str):
            return False
        else:
            return super(Predikaat_v??ide, self).__lt__(self,other)
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
        return Predikaat_v??ide(self.nimi,args)
class E(Symbol):#TODO: v??iks ka funktsioon olla, mis kohe lihtsustatud vormi tagastab(sama, mis mitte_??V praegu).
    def __new__(self,sisu):
        E=Symbol.__new__(self,"???("+str(sisu)+")")
        E.sisu=sisu
        return E
class Tipp:
    def __init__(self,predikaadid,EKd,m??rk):
        self.predikaadid=predikaadid#predikaadid #oluline, et k??ik erinevad predikaatv??ited siin oleksid erinevate hash'idega!
        self.EKd=EKd#eksistentsiaalsus_kvantorid
        self.m??rk=m??rk#Kas jaatatud v??i eitatud
    def __str__(self):
        sees=[]
        for pv in sorted(self.predikaadid.items(),key=lambda x:tuple([0]*isinstance(x[0],str)) or x[0].argumendid):
            if type(pv[1])==bool:
                sees.append((not pv[1])*"??"+str(pv[0]))
            else:
                sees.append("("+str(pv[0])+"="+pv[1]+")")
        for EK in self.EKd:
            sees.append(str(EK))
        return ((not self.m??rk)*"??")+"???("+" & ".join(sees)+")"
    def __repr__(self):
        return self.__str__()
    def suhteline_k??rgus(self):#TODO:saaab leida koos teega alluvateni.
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
    def alluvad_sabaga_eesj??rjestuses(self,eitustest_mitte_l??bi_minna=False,eitatute_harudesse_mitte_minna=False,laiendatuid_mitte_v??tta=True,leveleid=None,tipp_ise_ka=False):
        if leveleid==None:
            leveleid=float("inf")
        dq=[self]
        tee=[None]
        alluvad_eesj??rjestus=[]
        while dq:
            tipp=dq.pop()
            if tipp==True:
                tee.append(None)
                continue
            if tipp==False:
                tee.pop()
                continue
            tee[-1]=tipp
            alluvad_eesj??rjestus.append(tee.copy())
            dq.append(False)
            if (not eitatute_harudesse_mitte_minna or tipp.m??rk) and len(tee)<=leveleid:
                for EK in tipp.EKd[::-1]:
                    if (not eitustest_mitte_l??bi_minna or EK.m??rk) and (not laiendatuid_mitte_v??tta or EK.m??rk!="laiendatud"):
                        dq.append(EK)
            dq.append(True)
        if not tipp_ise_ka:
            alluvad_eesj??rjestus.pop(0)
        return alluvad_eesj??rjestus
    def t??ida_eitatud_asendus(self, algne_eitatud_tipp, leveleid,i,P1,alluvad_sabaga,tipp_kuhu_asendatakse_sabaga):

        ##
        P1_a=[]
        for s in tipp_kuhu_asendatakse_sabaga:
            for i_alluv in range(len(alluvad_sabaga)):
                if s==alluvad_sabaga[i_alluv][-1]:
                    P1_a.append(i_alluv)
        P1=P1_a+P1
        ##

        assert leveleid>=0
        if leveleid==0:
            return
        dq=[algne_eitatud_tipp[-1]]
        algne_tee=[None]
        uus_tee=[Tipp({},[],[]),self]
        while dq:
            tipp=dq.pop()
            if tipp == True:
                algne_tee.append(None)
                uus_tee.append(None)
                continue
            if tipp == False:
                algne_tee.pop()
                uus_tee.pop()
                continue
            algne_tee[-1] = tipp
            if len(algne_tee)!=1:#kui ei l??he esimest korda while-ts??klisse.
                uus_tee[-1]=Tipp({},[],None)
            uus_tee[-2].EKd.append(uus_tee[-1])
            uus_tee[-1].m??rk=algne_tee[-1].m??rk

            ###
            #TODO:pole l??puni implementeeritud. osad predikaatv??ited j????vad panemata.
            for predikaatv??ide,predikaatv??ite_v????rtus in algne_tee[-1].predikaadid.items():
                    #print("pv, tipus, mis on P1es madalaml v??i sama k??rgel ja puus k??rgemal v??i sama k??rgel kui alluvad_sabaga[P1[i1]].")#itereerib ??le k??igi predikaatv??idete, mis on P1es madalamal v??i sama k??rgel ja puus k??rgemal v??i sama k??rgel.
                    uute_predikaatv??idete_argumendid=[[]]
                    if isinstance(predikaatv??ide,Predikaat_v??ide):
                        for a in predikaatv??ide.argumendid:
                            if a>=len(algne_eitatud_tipp)-1:#kui a tipp on puus peale algset eitatud tippu
                                indexid_P1es=[a+2+i-len(algne_eitatud_tipp)]
                            else:#kui a tipp on puus enne algset eitatud tippu
                                #todo: siin viga.
                                #print("P1:",P1)
                                #print("tipp enne eitatud haru: a=",a," ; argumendi tipp=",algne_eitatud_tipp[a])
                                argumendi_tipp=algne_eitatud_tipp[a]#See tipp mille kvanteeritav argumendiks on.
                                #print("a:",a,"; a-tipp:",argumendi_tipp)
                                indexid_P1es=[]#N??itab, et mis indeksitel(see tipp v??i P1es mitu korda olla) argumendi(kvanteeritava) a tipp P1es on.
                                for i3 in range(i+1):
                                    #print("i3:",i3,"; alluvad_sabaga[P1[i3]][-1]:",alluvad_sabaga[P1[i3]][-1])
                                    if alluvad_sabaga[P1[i3]][-1]==argumendi_tipp:
                                        #Mis indeksil selle argumendi(kvanteeritava) kvantor(tipp) P1es on.
                                        indexid_P1es.append(i3+1)
                            #print("indexid_P1es:",indexid_P1es)
                            vana_uute_predikaatv??idete_argumendid=uute_predikaatv??idete_argumendid.copy()#todo:optimeerimiseks saab kopeerimise eemaldada.
                            uute_predikaatv??idete_argumendid=[]
                            for v in vana_uute_predikaatv??idete_argumendid:
                                for index_P1es in indexid_P1es:#TODO: lihtne lihtsustus
                                    uute_predikaatv??idete_argumendid.append(v+[index_P1es])
                            if not indexid_P1es:
                                #print("predikaatv??idet argumentidega",uute_predikaatv??idete_argumendid,"ei lisatud tippu",uus_tee[-1],", sest 1 selle argumendi tipp ei olnud asenduse harus. originaal:",predikaatv??ide)
                                break
                        else:
                            for uue_predikaatv??ite_argumendid in uute_predikaatv??idete_argumendid:
                                uus_tee[-1].predikaadid[Predikaat_v??ide(predikaatv??ide.nimi,uue_predikaatv??ite_argumendid)]=predikaatv??ite_v????rtus#+"l:"+str(P1[i1])+"i:"+str(P1[i2])
                                print("tipule",uus_tee[-1],"lisada predikaatv??ide",Predikaat_v??ide(predikaatv??ide.nimi,uue_predikaatv??ite_argumendid))
                                print("algne v??ide:",predikaatv??ide)
            ###
            dq.append(False)
            if len(uus_tee)<=leveleid+1:
                for EK in tipp.EKd[::-1]:
                    dq.append(EK)
            dq.append(True)
    @staticmethod
    def _teisenda_predikaatv??ited(laiendatud, P1, alluvad_sabaga, tipp_kuhu_asendatakse_sabaga):
        #P1e lisada tipp, kuhu asendatakse ja selle eelased.
        P1_a=[]
        for s in tipp_kuhu_asendatakse_sabaga:
            for i_alluv in range(len(alluvad_sabaga)):
                if s==alluvad_sabaga[i_alluv][-1]:
                    P1_a.append(i_alluv)
        P1=P1_a+P1

        for i2 in range(len(P1)):
            #print("eelneja P1es:",P1[i2])
            if alluvad_sabaga[P1[-1]][-1] in alluvad_sabaga[P1[i2]]:#alluvad[P1[i1]] ja alluvad[P1[i2]] on samal joonel puus. alluvad[P1[i2]] k??rgemal.
                #print(P1[i2],"(",i2,")","on madalamal P1es ja k??rgemal puus kui ",P1[-1],"(",-1,") ; P1=",P1)
                for predikaatv??ide,predikaatv??ite_v????rtus in alluvad_sabaga[P1[i2]][-1].predikaadid.items():
                    #print("pv tipus, mis on P1es madalaml v??i sama k??rgel ja puus k??rgemal v??i sama k??rgel kui alluvad_sabaga[P1[-1]]:",predikaatv??ide)#itereerib ??le k??igi predikaatv??idete, mis on P1es madalamal v??i sama k??rgel ja puus k??rgemal v??i sama k??rgel.
                    uute_predikaatv??idete_argumendid=[[]]
                    if isinstance(predikaatv??ide,Predikaat_v??ide):
                        for a in predikaatv??ide.argumendid:
                            argumendi_tipp=alluvad_sabaga[P1[i2]][a]#See tipp mille kvanteeritav argumendiks on.
                            indexid_puus=[]#N??itab, et mis indeksitel(see tipp v??i P1es mitu korda olla) argumendi(kvanteeritava) a tipp P1es on.
                            for i3 in range(len(P1)):#todo: v??i i2'eni itereerida?
                                if alluvad_sabaga[P1[i3]][-1]==argumendi_tipp:
                                    #Mis indeksil selle argumendi(kvanteeritava) kvantor(tipp) P1es on.
                                    indexid_puus.append(i3+1)
                            vana_uute_predikaatv??idete_argumendid=uute_predikaatv??idete_argumendid.copy()#todo:optimeerimiseks saab kopeerimise eemaldada.
                            uute_predikaatv??idete_argumendid=[]
                            for v in vana_uute_predikaatv??idete_argumendid:
                                for index_P1es in indexid_puus:
                                    uute_predikaatv??idete_argumendid.append(v+[index_P1es])
                            if not indexid_puus:
                                #print("predikaatv??idet argumentidega",uute_predikaatv??idete_argumendid,"ei lisatud tippu",P1[i1],"(",i1+1,"), sest 1 selle argumendi tipp ei olnud asenduse harus. originaal:",pv)
                                break
                        else:
                            for uue_predikaatv??ite_argumendid in uute_predikaatv??idete_argumendid:
                                if len(P1) in uue_predikaatv??ite_argumendid:
                                    laiendatud[len(P1)-len(tipp_kuhu_asendatakse_sabaga)+1].predikaadid[Predikaat_v??ide(predikaatv??ide.nimi,uue_predikaatv??ite_argumendid)]=predikaatv??ite_v????rtus#+"l:"+str(P1[i1])+"i:"+str(P1[i2])
                                    #print("tipule",P1[-1],"(",len(P1),")","lisada predikaatv??ide",Predikaat_v??ide(predikaatv??ide.nimi,uue_predikaatv??ite_argumendid))
                                    #print("algne v??ide:",predikaatv??ide,"algne tipp:",P1[-1],"(",i2+1,")\n")
                                #else:
                                    #print("predikaatv??idet argumentidega",uue_predikaatv??ite_argumendid,"ei lisatud tippu",P1[-1],"(", len(P1), "), sest seal polnud vastava tippu kvanteeritavat.\n")
    def laiendatud_EKd(self, tipp_sabaga):#FAILIS "alternatiivsed funktsioonid.py" on teistsugune ja vb. efektiivsem implementatsioon sellest funktsioonist.
        #self peaks funktsiooni kutsel olema LR
        alluvad_sabaga=self.alluvad_sabaga_eesj??rjestuses(eitatute_harudesse_mitte_minna=True)
        ###
        for i_alluv in range(len(alluvad_sabaga)):
            alluvad_sabaga[i_alluv][-1].predikaadid["n"]=str(i_alluv)
        ###

        suhteline_k??rgus=0
        for eitatud_EK in tipp_sabaga[-1].EKd:
            if not eitatud_EK.m??rk:
                eitatud_haru_k??rgus=eitatud_EK.suhteline_k??rgus()
                if eitatud_haru_k??rgus>suhteline_k??rgus:
                    suhteline_k??rgus=eitatud_haru_k??rgus
        #print("eitatud harude max k??rgus:",suhteline_k??rgus)

        if suhteline_k??rgus==0:
            return ()

        tipu_max_index=len(alluvad_sabaga)-1

        kaadrid.append(deepcopy(kaader))
        P1=[0]*suhteline_k??rgus#TODO: peaks ka tipu, kuhu asendatakse eelaste indeksid P1'e panema.
        laiendatud=[tipp_sabaga[-1],Tipp({"laiendatud":"0"},[],"laiendatud")]
        laiendatud[-2].EKd.append(laiendatud[-1])

        Tipp._teisenda_predikaatv??ited(laiendatud,P1[:1],alluvad_sabaga,tipp_sabaga)
        for i_laiendatud_tipp in range(1,suhteline_k??rgus):
            laiendatud.append(Tipp({"laiendatud":"0"},[],True))
            Tipp._teisenda_predikaatv??ited(laiendatud,P1[:i_laiendatud_tipp+1],alluvad_sabaga,tipp_sabaga)
            laiendatud[-2].EKd.append(laiendatud[-1])
        kaadrid.append(deepcopy(kaader))
        #print("muuta: [P1, P1, 'P1']")

        while 1:
            i=suhteline_k??rgus-1
            print("P1:", P1)
            while i>=0:
                print("P1[i]:", P1[i], " ; tipu_max_index:", tipu_max_index)
                if P1[i]==tipu_max_index:
                    print("0iks P1:", P1)
                    P1[i]=0
                    i-=1
                else:
                    print("suurendada P1:", P1)
                    assert P1[i]<tipu_max_index
                    P1[i]+=1
                    #muutused=P1.copy()#ajutine
                    if i==0:
                        if not alluvad_sabaga[P1[i]][-1].m??rk:
                            print("positsioonil", i, "on eitatud haru nr", P1[i], ":", alluvad_sabaga[P1[i]][-1])
                            continue#mitte lisada seda laiendatudesse
                        yield laiendatud[1]
                    for i in range(i,suhteline_k??rgus):#siin loopis uuendatakse laiendatuid.
                        #muutused[i]="P"+str(muutused[i])
                        laiendatud[i+1]=Tipp({"laiendatud":str(P1[i])},[],alluvad_sabaga[P1[i]][-1].m??rk)
                        if i==0:
                            #print(":::",laiendatud[i].m??rk)
                            #assert laiendatud[i].m??rk==True
                            laiendatud[1].m??rk="laiendatud"
                        laiendatud[i].EKd.append(laiendatud[i+1])
                        #print("haru nr:",P1[i_2],alluvad_sabaga[P1[i_2]])
                        Tipp._teisenda_predikaatv??ited(laiendatud,P1[:i+1], alluvad_sabaga,tipp_sabaga)
                        if not alluvad_sabaga[P1[i]][-1].m??rk:#kui lisatakse eitatud haru P1'e, siis ei sellest paremale P1'e enam midagi ei tohiks lisada.#todo:kui esimene haru alluvate j??rjendis on eitatud, siis vist ei l??he siia.
                            print("positsioonil",i,"on eitatud haru nr",P1[i],":",alluvad_sabaga[P1[i]][-1])
                            #print("muuta:", muutused)
                            laiendatud[i+1].t??ida_eitatud_asendus(alluvad_sabaga[P1[i]],suhteline_k??rgus-i-1,i,P1,alluvad_sabaga,tipp_sabaga)
                            kaadrid.append(deepcopy(kaader))
                            break
                    else:#kui polnud eitatuid.
                        print("polnud eitatuid")
                        #print("muuta:",muutused)
                        break#SIHTPUNKTI 2
            else:#k??ik numbrid olid maximum(radix) v????rtusega.
                print("L??pp, sest madalaim lubatud P1 ideks sai nullitud.")
                yield laiendatud[1]
                for i_alluv in range(len(alluvad_sabaga)):
                    del alluvad_sabaga[i_alluv][-1].predikaadid["n"]
                return
            #print("muuta:",muutused)#SIHTPUNKT2
            kaadrid.append(deepcopy(kaader))
            #print("laiendatud:",laiendatud)
    def t??psem_kui(self, other):
        for EK_o in other.predikaadid:
            for EK_s in self.predikaadid:
                if EK_s==EK_o:
                    break
            else:
                return False
        for EK_o in other.EKd:
            for EK_s in self.laiendatud_EKd():
                if EK_s>>EK_o:
                    break
            else:
                return False
        for EK_o in other.eitatud_EKd:
            for EK_s in self.eitatud_EKd:
                if EK_o>>EK_s:
                    break
            else:
                return False
        return True
    @staticmethod
    def _asenduste_valikud(v??imalikke_v????rtusi):
        num=[]
        for i in v??imalikke_v????rtusi:
            if i==None:
                num.append(-1)
            else:
                num.append(0)
        while True:
            yield num
            for i in range(0,len(v??imalikke_v????rtusi)):
                if num[i]==v??imalikke_v????rtusi[i]:
                    num[i]=0
                elif v??imalikke_v????rtusi[i]!=None:
                    num[i]+=1
                    break
            else:
                return
    def mitte_??V(self):
        #TODO:Saab puu koostamisega kokku panna ja kontrollida ??Vd juba enne t??ielikku parssimist.
        #TODO:Need harud v??ib eemaldada, mille olemasolu saab j??reldada teisi mingi j??rjekorras valides.
        #TODO:saab asendada ka eitatud kvantoreid. Kahe P1 elemendi vaheline seos ei s??ili, kui esimesest(P1'es v??iksema indeksiga) teise minemiseks tuleb tagurpidi l??bida eitatud haru.
        for tipp_sabaga in self.alluvad_sabaga_eesj??rjestuses(eitustest_mitte_l??bi_minna=True,tipp_ise_ka=True):
            tipp_??V=False
            #todo:Kui laiendatud_EKsse tuleb eitatud kvanto poolikult(k??rgemad oksad puudu), siis see tugvendab eitatud_EKd, ja muudab algoritmi valeks.
            for EK in self.laiendatud_EKd(tipp_sabaga):
                print(EK)
                print()
                continue
                for eitatud_EK in self.EKd:
                    if not eitatud_EK.m??rk:
                        #sisud_koosk??las=Tipp().mitte_??V()
                        #koosk??las ehk not EK_sisust_j??reldub_eitatud_EK_eitatud_sisu
                        sisud_koosk??las,EK_sisust_j??reldub_eitatud_EK_sisu=Tipp.v??dle(EK, eitatud_EK)
                        if sisud_koosk??las:#kui pole kindel, et asjal, mille eksisteerimist EK v??idab ei pea selleks, et selle eksisteerimine eitatud EK poolt keelatud poleks, olema omadusi, mida EK sisus pole kirjeldatud ja selleks ei pea sellega seoses uusi asju eksisteerima v??i mitte eksisteerima.
                            #sellest, mis EK sees otseselt kirjas on ei piisa, et j??reldada, et EK poolt kirjeldatu eksisteerimine pole eitatud EK poolt keelatud.
                            if EK_sisust_j??reldub_eitatud_EK_sisu:#EK t??psem v??i v??rdne kui eitatud_EK(ja koosk??las).
                                #self.EKd.pop(0)
                                tipp_??V=True
                                break#LR on ??V
                            else:#eitatud_EK t??psem kui EK v??i eitatud_EK on t??psuselt v??rreldamatu EKga.
                                # kui EK kirjeldatud:
                                #    asjal peavad olema mingid predikaat v??ited,
                                #    asjaga seoses peavad muud asjad eksisteerima v??i
                                #    muud asjad ei tohi selle asjaga mingil viisil seotud olles eksisteerida
                                # et EK kirjeldatud asja eksiteerimine poleks eitatud EK poolt eitatud
                                # ja seda pole EK sees otseselt kirjas.
                                pass#Luua uusi LRe, EKsse on lisatud vastasm??rgiga eitatud_EK harusid, et EK ja eitatud_EK sisud ei oleks koosk??las.
    #                    else:
    #                        pass#sellest, mis EK sees otseselt kirjas on piisab, et j??reldada, et see pole eitatud EK poolt keelatud.
                if tipp_??V:
                    break
            if tipp_??V:
                break
        #Tree_Visualize(kaadrid)
        #kaadrid.append(deepcopy(LV))
        return []#True
class LV:
    def __init__(self,seos):
        if isinstance(seos,Boolean):
            self.predikaadid={"LV":True}
            self.LRid=LV.koosta_puu(seos)
        else:
            raise NotImplementedError
    def __str__(self):
        sees=[]
        for ek in self.LRid:
            sees.append(str(ek))
        return " | ".join(sees)
    def __repr__(self):
        return self.__str__()
    def mitte_??V(LV):
        #TODO:kui laiendada Expr klassi siis saab selle ehk klassimeetodiks teha. Et seda saaks otse Sympy avaldistele v??i klassi E objektidele rakendada.
        #TODO:Saab puu koostamisega kokku panna ja kontrollida ??Vd juba enne t??ielikku parssimist.
        global kaadrid,kaader
        kaader=LV
        kaadrid=[deepcopy(LV)]
        print("LV:",LV)
        #Tree_Visualize(kaadrid)
        while LV.LRid:
            LR=LV.LRid[0]
            juurde_tekitatud_harud=LR.mitte_??V()
            if juurde_tekitatud_harud==True:
                return True
            LV.LRid.pop(0)
            LV.LRid+=juurde_tekitatud_harud

        Tree_Visualize(kaadrid)


        return False
    def __bool__(self):
        if not self.mitte_??V():
            return False
        elif not (~self).mitte_??V():
            return True
        else:
            raise Exception("Unkown if true or false.")
    @staticmethod
    def _jaota_osadesse(boolean_v??ide):
        boolean_v??ide=to_dnf(boolean_v??ide.simplify(),True)
        if type(boolean_v??ide)==Or:
            boolean_v??ide=boolean_v??ide.args
        elif boolean_v??ide==True:
            yield ({},[],[])
            return
        else:
            boolean_v??ide=[boolean_v??ide]
        #print("j??rjend omavahel ORiga eraldatud olnud osadest:",boolean_v??ide)
        for dnf_element in boolean_v??ide:
            if type(dnf_element)==And:
                sisu=dnf_element.make_args(dnf_element)
            else:
                sisu=[dnf_element]
            predikaadid={}
            eitatud_Ed=[]
            Ed=[]
            #print("j??rjend omavahel ANDiga eraldatud olnud osadest:",sisu)
            for jaatuse_element in sisu:
                t????p=type(jaatuse_element)
                if t????p==E:
                    Ed.append(jaatuse_element)
                elif t????p==Not:
                    if type(jaatuse_element._args[0])==E:
                        eitatud_Ed.append(jaatuse_element._args[0])#TODO:peaks sisemiselt, mitte v??liselt eitama.
                    else:
                        assert type(jaatuse_element._args[0])==Predikaat_v??ide
                        predikaadid[jaatuse_element._args[0]]=False
                else:
                    assert t????p==Predikaat_v??ide
                    predikaadid[jaatuse_element]=True
            yield (predikaadid,eitatud_Ed,Ed)
    @staticmethod
    def koosta_puu(seos, k=0):
        sisemised_kvantorid=[]
        sisemiste_kvantorite_v??itatud_vormid=[]
        for sisemine_kvantor in seos.atoms():
            if type(sisemine_kvantor)==E:
                sisemised_kvantorid.append(sisemine_kvantor)
                vv=LV.koosta_puu(sisemine_kvantor.sisu,k+1)
                sisemiste_kvantorite_v??itatud_vormid.append(vv)
        #print(seos, " :sisemiste_kvantorite_v??itatud_vormid:", sisemiste_kvantorite_v??itatud_vormid)
        #print("type:", t2ype(seos), "; plato:", seos, ";")
        v??itatud_vormid=[]
        for sisemise_v??ituse_elemendi_p_osa,sisemise_v??ituse_elemendi_u_osa,sisemise_v??ituse_elemendi_e_osa in LV._jaota_osadesse(seos):
            #print("osa:",sisemise_v??ituse_elemendi_p_osa,sisemise_v??ituse_elemendi_u_osa,sisemise_v??ituse_elemendi_e_osa)
            for i_sisemine_kvantor in range(len(sisemise_v??ituse_elemendi_u_osa)):#teeb asendused U-osas.
                #TODO:PEAB need ??heks kvantoriks ??hendama, et saaks teada, kas midagi saab k??rgemalt alla poole tuua.
                eitatud_ek=sisemise_v??ituse_elemendi_u_osa.pop(0)
                #print("    eitatud kvantor:",eitatud_ek)
                for variant in sisemiste_kvantorite_v??itatud_vormid[sisemised_kvantorid.index(eitatud_ek)]:
                    sisemise_v??ituse_elemendi_u_osa.append(variant)
                    sisemise_v??ituse_elemendi_u_osa[-1].m??rk=False
                    #print("      u-ossa lisada:",variant," ; T????P=",type(variant))
            asenduste_valik=[None]*len(sisemised_kvantorid)
            for sisemine_kvantor in sisemise_v??ituse_elemendi_e_osa:#m????rab, et kui palju variante kui mitmenda kvantori asendamiseks E-osas on.
                i=sisemised_kvantorid.index(sisemine_kvantor)
                asenduste_valik[i]=len(sisemiste_kvantorite_v??itatud_vormid[i])-1
            for asenduste_valik in Tipp._asenduste_valikud(asenduste_valik):
                v??limise_v??ituse_elemendi_e_osa=[]
                for i in range(len(asenduste_valik)):#TODO: asendada ainult muutunud indeksitega(asenduste valikus) kvantorid.
                    if asenduste_valik[i]!=-1:#k??ik ja ainult U'd asendatakse mingi Plato'e v??i predikaatide vahelise booleanseosega.
                        #print("    asendada:",sisemised_kvantorid[i],":",sisemiste_kvantorite_v??itatud_vormid[i][asenduste_valik[i]])
                        v??limise_v??ituse_elemendi_e_osa.append(deepcopy(sisemiste_kvantorite_v??itatud_vormid[i][asenduste_valik[i]]))
                v??itatud_vormid.append(Tipp(sisemise_v??ituse_elemendi_p_osa,v??limise_v??ituse_elemendi_e_osa+sisemise_v??ituse_elemendi_u_osa,True))
        #print("  v??itatud vormid:",v??itatud_vormid)
        if v??itatud_vormid:
            return v??itatud_vormid
        return [False]


if __name__=="__main__":
    if False:
        on_null=Predikaat("on_null")
        v??rdne=Predikaat("v??rdne")
        PEANO=E(on_null(1))&\
              ~E(~v??rdne(1,1))&\
              ~E(E(E(~((v??rdne(1,2)&v??rdne(2,3))>>v??rdne(3,1)))))
        peano_puu=LV(PEANO).mitte_??V()
        print("Peano tulem:", peano_puu)
        print("\n#####\n")

    A=Predikaat("A")
    B=Predikaat("B")
    #print(koosta_puu(E(A(1) & A(1, 1) & E(A(1, 2) & E(A(2, 3) & A(3, 1))))))

    if False:# v??ituste v??lja viimine ilma ??V-kontrolliteta.
        print("################################\nTESTS:")
        sisendid=[~E(A(21)&A(22)&A(23)),E(E(E(E(A(0)|A(1)|A(2))))),
                  (E(A(30)&A(31))|(A(33)&E(A(40)|A(41)&E(E(E(A(51)|A(53))))))),
                  ~E(A(1)&A(2)),
                  ~E(A(1) | A(2) & A(3)) & E(A(4) & A(5) & E(A(6))),
                  A(10)&E(A(11)>>A(12)&~E(A(13)|A(14)&~E(A(10)&A(20)))),
                  E(v??rdne(0)&on_null(2)&on_null(1)),
                  ~E(A(2)<<A(1)),E(A(1) | A(2)) & E(A(1) | A(2))]
        oodatud=["[(?????((A(21) & A(22) & A(23))))]",
                 "[(???((???((???((???((A(0)))))))))), (???((???((???((???((A(1)))))))))), (???((???((???((???((A(2))))))))))]",
                 "[(???((A(30) & A(31)))), (A(33)&???((A(40)))), (A(33)&???((A(41)&???((???((???((A(51)))))))))), (A(33)&???((A(41)&???((???((???((A(53))))))))))]",
                 "[(?????((A(1) & A(2))))]",
                 "[(?????((A(1)))&?????((A(2) & A(3)))&???((A(4) & A(5)&???((A(6))))))]",
                 "[(A(10)&???((A(12)&?????((A(13)))&?????((A(14)&?????((A(10) & A(20)))))))), (A(10)&???((??A(11)&?????((A(13)))&?????((A(14)&?????((A(10) & A(20))))))))]",
                 "[(???((on_null(1) & on_null(2) & v??rdne(0))))]",
                 "[(?????((A(2)))&?????((??A(1))))]",
                 "[(???((A(1)))), (???((A(2))))]"]
        for i in range(max(len(sisendid),len(oodatud))):
            tulemus=str(LV.koosta_puu(sisendid[i]))
            if tulemus!=oodatud[i]:
                print("SISEND :",sisendid[i])
                print("TULEMUS:",tulemus)
                print("OODATUD:",oodatud[i])
                print()
                #print(sisendid[i],":",tulemus,":",oodatud[i])
            print()
        # proov=mitte_??V(U(A(0)&A(1)&U(A(3)&A(4)&U(A(5)))&~U(A(21)&A(22)&U(A(23))&~U(A(24)|A(25)))))
        # print("proov:",mitte_??V(U(U(on_null(2))&U(v??rdne(2,2)))))
        # proov2=mitte_??V(U(U(U(U(A(0)&A(1)&A(2))))))
        #    proov2=mitte_??V(~U(A(0) | A(1) | A(2)))
        # print("proov:", proov2)
    if 1:
        #assert not LV(E(A(1))&~E(A(1)))<.mitte_??V()
        #assert LV(~(E(A(1))&~E(A(1)))).mitte_??V()
        #assert not LV(E(A(1)&B(1))&~E(A(1))).mitte_??V()
        #assert LV(E(A(1))&~E(A(1)&B(1))).mitte_??V()
        #assert LV(~E(A(0)&E(A(0)&E(A(0))))&E(A(1)&E(~A(1))&E(A(2)))&E(B(4)&E(~A(4)&A(6))&E(~A(6)&A(8))&E(~A(8)&B(10))&E(B(11)&B(12))&~E(B(13)&B(14)))&E(~A(15)&E(A(30)))&E(~B(16)&E(A(17)&E(A(18)))&E(A(19)&E(A(20))&E(A(21))))).mitte_??V()

        # vist O'ga ??V kontroll annab vale tulemuse (tegelt ??V).
        #assert not LV(E(~A(1, 1) & E(A(1, 2) & ~A(2, 1) & ~A(2, 2) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & ~A(3, 3)) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3)))) & ~E(~A(1, 1) & E(~A(1, 2) & A(2, 1) & ~A(2, 2) & E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & ~A(3, 3)) & E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3))))).mitte_??V()
        #visualiseerimise viga. osad tippude parameetrid katavad teisi.

        #LV(E(~E(A(7)))&E(~A(1, 1)&~E(A(7)) & E(A(1, 2) & ~A(2, 1) & ~A(2, 2) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & ~A(3, 3)) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3))))).mitte_??V()
        #assert not mitte_??V(E(A(1,1)&~E(~(A(2,2)&~A(1,2)&~A(2,1)))))#tegelt ??V
        #assert not mitte_??V(E(A(1,1)&~E(~(A(2,2)&A(1,2)&~A(2,1)))))#tegelt ??V
        #assert not mitte_??V(E(A(1,1)&~E(~(A(2,2)&~A(1,2)&A(2,1)))))#tegelt ??V

        #assert not mitte_??V(E(A(1, 1)&~E(~(A(2, 2)>>(~A(1, 2)&A(2, 1))))))#tegelt ??V
        #M=Predikaat("x1???le meeldib x2")#on: x_1???le meeldib x_2
        #on_mari=Predikaat("x1 on mari")
        #LV(E(on_mari(1) & ~E(M(1, 2) & E(M(1, 3) & ~M(2, 3) & M(3, 1)) & E(M(1, 3) & M(2, 3)) & ~E(M(2, 3) & M(3, 3))))&
        #   E(E(on_mari(2)&M(2,1)&E(M(1,3)&M(2,3))&E(M(2,3)&M(3,2)&~M(1,3)))&~E(M(2,1)&M(2,2)))
        #   | E(M(1,1)&~E(M(1,2)&M(2,2)&M(2,1)))).mitte_??V()
        #[k??igil, kes Marile meeldivad,[ei ole kedagi kes Marile meeldiks, aga temale mitte ja kellele meeldiks Mari] v??i [ei ole kedagi, kes nii talle kui Marile meeldiks] v??i [on keegi, kes neile meeldib ja kes iseendale meeldib]] ja
        #ja leidub keegi, kes meeldib marile, nii, et eksisteerib [keegi, kes meeldib nii marile kui talle] ja [keegi, kes meeldib marile, kellele mari meeldib ja kelle ei meeldi talle] ja ei leidu kedagi, kes nii iseendale kui ka talle ta meeldiks
        #v??i [on keegi(x_1) kes endale meeldib, aga [kellel pole kedagi kes nii talle kui iseendale meeldiks ja kellele meeldiks tema(x_1)]]


        #assert (mitte_??V(U(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))&E(A(1,1)&U(A(2,2)&~A(1,2)&~A(2,1))&E(A(2,2)&~A(1,2)&~A(2,1)))))#tegelt ??V?

        #LV(E(A(1))&E(A(2)|A(3))).mitte_??V()
        #LV(~E(E(E(A(1,2,3)))&A(1,1,1)|E(~A(2,2,1)|~A(1,1,2)&~E(A(3,3,3)&A(3,2,1)))|E(A(2,2,2)&~A(2,1,2)&A(2,2,1))&E(A(2,1,2)&A(2,2,1)|~A(2,2,2)&A(2,1,1)|E(A(3,2,3)&A(3,1,3))))).mitte_??V()
        #LV(~E(E(E(A(1,2,3)))&A(1,1,1)|E(~A(1,1,2)&~E(A(3,3,3)&A(3,2,1)))|E(A(2,2,2)&~A(2,1,2)&A(2,2,1))&E(A(2,1,2)&A(2,2,1)))).mitte_??V()

        #LV(~E(~A(1,1)&E(~A(2,2)&A(1,2)&A(2,1)))&~E(A(1,1)&E(A(2,2)&A(1,2)&~A(2,1)))&~E(~A(1,1)&E(~A(2,2)&~A(1,2)&~A(2,1)))&  E(E(~A(2,2)&A(1,2)&A(2,1))&E(A(2,2)&~A(1,2)&E(A(3,3)&~A(3,2)&~A(2,3)&A(1,3)&A(3,1))&E(~A(3,3)&A(3,2)&A(2,3)&~A(1,3)&~A(3,1)&E(A(4,4)&A(2,4)&~A(4,2)&~A(1,4)&A(4,1)))))).mitte_??V()
        #??V: P1=[1,3]
        #kuna A(1,1) on eitatud harus m????ramata, siis jaatatus harus predikaatv??ited x1'ega pole siin olulised.
        #visualiseerimise viga. osad tippude parameetrid katavad teisi.

        #LV(~E(E(A(1)&E(A(2)&E(A(3)&E(A(4)&E(A(5)&E(A(6)&E(A(7)))))))))&E(A(1))).mitte_??V()

        #BUG:
        #LV(E(A(1)&E(~A(1,2)&~E(~A(1,2,3)&E(~A(1,2,3,4)&E(~A(1,2,3,4,5))))))).mitte_??V()

        #BUG:
        #assert not LV(E(~A(1,1)&E(~A(2,2)&E(A(2,3)&~A(3,2)&~A(3,3)))&~E(E(~A(3,2))&~A(2,2)&E(~A(2,3)&A(3,2)&~A(3,3)&E(A(2,4)&~A(3,4)&~A(4,2)&~A(4,3)&A(4,4)))))).mitte_??V()

        #assert not LV(E(~A(1, 1) & E(A(1, 2) & ~A(2, 1) & ~A(2, 2))) & ~E(E(~A(2,1))&~A(1, 1) & E(~A(1, 2) & A(2, 1) & ~A(2, 2)&E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3))))).mitte_??V()

        #eitatu t??hi:
        #LV(E(A(1,1)&E(A(2,1)&~A(1,2)&~E(A(3,2)&A(3,1))))).mitte_??V()
        #LV(E(A(1) & E(~A(1, 2) & ~E(~A(1, 2, 3))))).mitte_??V()
        assert not LV(E(~A(1,1)&E(~A(2,2)&E(A(2,3)&~A(3,2)&~A(3,3)))&~E(E(~A(3,2)&A(1,3))&~A(2,2)&E(~A(2,3)&A(3,2)&~A(3,3)&E(~A(1,4)&A(2,4)&~A(3,4)&~A(4,2)&~A(4,3)&A(4,4)))))).mitte_??V()