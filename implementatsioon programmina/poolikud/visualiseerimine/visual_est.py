import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import deque
import gc

class Tipp:
    def __init__(self, predikaadid, eitatud_EKd, EKd):
        self.predikaadid = predikaadid
        self.eitatud_EKd = eitatud_EKd
        self.EKd = EKd

def get_predikaadid(vertex):#My CHANGED FUNCTION
    final_str=""
    if(isinstance(vertex.predikaadid, list)):
        v=vertex.predikaadid[::-1]
    elif(isinstance(vertex.predikaadid, dict)):
        v=vertex.predikaadid.values()
    for i in v:
        if i==False:
            final_str+="-"
        elif i==True:
            final_str+="+"
        else:
            final_str+=i
        final_str+="\n"
    return final_str[:-1]

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
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
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def objects_by_id(id_):
    for obj in gc.get_objects():
        if id(obj)==id_:
            return obj

def fill_the_gaps_of_the_param_tree(G,root,labeldict):
    count=1
    while True:
        level_nodes=[]
        level_predikaadid=[]
        nodes = set(nx.ego_graph(G, id(root), radius=count))
        nodes -= set(nx.ego_graph(G, id(root), radius=count-1))
        nodes=list(nodes)
        if len(nodes) == 0:
            break
        else:
            for node in nodes:
                node_obj = objects_by_id(node)
                if (isinstance(node_obj.predikaadid, dict)):
                    level_nodes.append(node_obj)
                    level_predikaadid.extend(node_obj.predikaadid.keys())
            level_predikaadid=list(set(level_predikaadid))
            final_level_predikaadid=[]
            for param in level_predikaadid:
                match=False
                for param1 in final_level_predikaadid:
                    try:
                        print(param,param1)
                        if param==param1:
                            match=True
                    except Exception as e:
                        print(e)
                if match==False:
                    final_level_predikaadid.append(param)
            try:
                final_level_predikaadid.sort(reverse=True)
            except Exception as e:
                print(e)
            node_count=0
            for node in nodes:
                node_obj = objects_by_id(node)
                if(isinstance(node_obj.predikaadid, dict)):
                    labels=[]
                    for key_name in final_level_predikaadid:
                        if key_name in node_obj.predikaadid.keys():
                            if node_obj.predikaadid[key_name] == False:  # MINU MUUTUS
                                labels.append("-")
                            elif node_obj.predikaadid[key_name] == True:  # MINU MUUTUS
                                labels.append("+")
                            else:  # MINU MUUTUS
                                labels.append(node_obj.predikaadid[key_name])
                        else:
                            keycount = 0
                            for keyvalue in node_obj.predikaadid.keys():
                                if keyvalue==key_name:
                                    if node_obj.predikaadid[keyvalue]==False:  # MINU MUUTUS
                                        labels.append("-")
                                    elif node_obj.predikaadid[keyvalue]==True:  # MINU MUUTUS
                                        labels.append("+")
                                    else:  # MINU MUUTUS
                                       labels.append(node_obj.predikaadid[keyvalue])
                                    keycount=keycount+1
                            if(keycount==0):
                                labels.append(" ")
                    if node_count==0:
                        labeldict[id(node_obj)]='\n'.join(labels)
                    else:
                        labeldict[id(node_obj)]='\n'.join(labels)
                    node_count+=1
            max_predikaadid=0
            for node in nodes:
                if(labeldict[node].count('\n')>max_predikaadid):
                    max_predikaadid=labeldict[node].count('\n')
            print(max_predikaadid)
            for node in nodes:
                print(labeldict[node],max_predikaadid)
                labeldict[node]='\n'*int(max_predikaadid-labeldict[node].count('\n'))+labeldict[node]
        count=count+1

class Tree_Visualize:
    def __init__(self,vertex):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.root_vertex = vertex
        self.generate_tree()
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def generate_tree(self):
        f = plt.figure()
        f.add_subplot(111)
        G = nx.Graph()
        dq = deque([self.root_vertex])
        type2_edge_labels = {}
        labeldict={}
        while(dq):
            vert = dq.pop()
            labeldict[id(vert)]=get_predikaadid(vert)
            for j in range(len(vert.eitatud_EKd)):
                G.add_edge(id(vert), id(vert.eitatud_EKd[j]))
                dq.appendleft(vert.eitatud_EKd[j])
            for k in range(len(vert.EKd)):
                G.add_edge(id(vert), id(vert.EKd[k]))
                type2_edge_labels[id(vert), id(vert.EKd[k])] = 'x'
                dq.appendleft(vert.EKd[k])
        fill_the_gaps_of_the_param_tree(G,self.root_vertex,labeldict)
        pos = hierarchy_pos(G, id(self.root_vertex))
        flipped_pos = {node: (x, -y) for (node, (x, y)) in pos.items()}
        nx.draw(G, pos=flipped_pos,font_size=7, node_size=2300, node_color='white',labels=labeldict, with_labels=True)
        nx.draw_networkx_edge_labels(G, flipped_pos, edge_labels=type2_edge_labels, font_color='red')
        plt.subplots_adjust(top=1.05,right=1.05,left=-0.05,bottom=-0.05,hspace=0,wspace=0)
        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both',
                                    expand=1)  # `side='top', fill='both', expand=1` will resize plot when you resize window
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand=1)


class Something:
   def __init__(self,s):
       self.s=s
   def __eq__(self, other):
       return self.s == other.s
   def __lt__(self, other):
       return self.s<other.s
   def __hash__(self):
       return hash(self.s)

if __name__ == '__main__':
    if False:
        s1 = Something(1)
        s2 = Something(1)
        S1 = Something(2)
        S2 = Something(2)
        v_x = Tipp(['1', '2', '3', '4'], [], [])
        v0_1_1 = Tipp({None: "9"}, [], [])
        v0_1 = Tipp({s1: "1", S1: "2"}, [v0_1_1], [])
        v0_2 = Tipp({s1: "3", S2: "4"}, [], [])
        v0_3_1 = Tipp({None: "N"}, [], [])
        v0_3_2 = Tipp({True: "T"}, [], [])
        v0_3_p0 = Tipp({None: "n", True: "t"}, [], [])
        v0_3_p1 = Tipp({None: "n", False: "f"}, [], [])
        v0_3 = Tipp({s2: "5", S2: "6"}, [v0_3_p0, v0_3_p1], [v0_3_1, v0_3_2])
        v0_4 = Tipp({s2: "7", S1: "9"}, [], [])
        v0 = Tipp({}, [v0_1, v0_2, v0_3, v_x], [v0_4])
        app = Tree_Visualize(v0)
    if True:
        v0_0 = Tipp({1: "0:1", 5: "0:5", 6: "0:6"}, [], [])
        v0_1 = Tipp({1: "1", 2: "2", 4: "4", 5: "5", 6: "6"}, [], [])
        v0_2 = Tipp(["l", "o", "w"], [], [])
        v0 = Tipp(["r", True, True, "t"], [v0_1, v0_2], [v0_0])
        app = Tree_Visualize(v0)