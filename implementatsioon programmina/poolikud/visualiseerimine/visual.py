#TODO: special field in vertexes to indicate if the vertex must be under or above a special horisontal line. May assume that branches o of vertixes that are over line are also always over line.
#TODO: crossing out type2 edges should cover type1 edges.
import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import deque
import gc

class Tipp:
    def __init__(self, predikaadid, EKd, eitatud_EKd):
        self.predikaadid = predikaadid
        self.EKd = EKd
        self.eitatud_EKd = eitatud_EKd


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
        self.window.bind("<Right>",lambda x:self.frames_swich(1))
        self.window.bind("<Left>",lambda x:self.frames_swich(-1))
        self.canvas = FigureCanvasTkAgg(self.f, master=self.window)
        self.canvas.get_tk_widget().pack(side='top', fill='both',expand=1)  # `side='top', fill='both', expand=1` will resize plot when you resize window
        toolbar=NavigationToolbar2Tk(self.canvas, self.window)
        toolbar.update()
        self.frames=frames
        self.i_frame=0
        self.root_vertex = self.frames[0]
        self.generate_tree()
        self.window.mainloop()
    def frames_swich(self,n_frames_to_swich):
        self.i_frame+=n_frames_to_swich
        self.window.title("frame:"+str(self.i_frame))

        #for item in self.canvas.get_tk_widget().find_all():
        #    self.canvas.get_tk_widget().delete(item)
        self.f.clear()

        if self.i_frame<len(self.frames):
            self.root_vertex=self.frames[self.i_frame]
            self.generate_tree()
        else:
            print("Nii palju kaadreid pole:", self.i_frame)
    def quit(self,event):
        self.window.destroy()
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
    def generate_tree(self):
        G = nx.Graph()
        dq = deque([self.root_vertex])
        type2_edge_labels = {}
        labeldict={}
        to_end_of_lv=1
        while dq:
            vert = dq.pop()
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
                for branch in range(len(vert.EKd)):
                    G.add_edge(id(vert), id(vert.EKd[branch]))
                    dq.appendleft(vert.EKd[branch])
            else:
                for branch in range(len(vert.EKd)):
                    G.add_edge(id(vert), id(vert.EKd[branch]))
                    dq.appendleft(vert.EKd[branch])
                for branch in range(len(vert.eitatud_EKd)):
                    G.add_edge(id(vert), id(vert.eitatud_EKd[branch]))
                    type2_edge_labels[id(vert), id(vert.eitatud_EKd[branch])] = 'x'
                    dq.appendleft(vert.eitatud_EKd[branch])
        Tree_Visualize.fill_the_gaps_of_the_param_tree(G,self.root_vertex,labeldict)
        pos = Tree_Visualize.hierarchy_pos(G, id(self.root_vertex))
        flipped_pos = {node: (x, -y) for (node, (x, y)) in pos.items()}
        nx.draw(G, pos=flipped_pos,font_weight="bold",font_size=7, node_size=2300, node_color='white',labels=labeldict, with_labels=True)
        nx.draw_networkx_edge_labels(G, flipped_pos, edge_labels=type2_edge_labels, font_color='red')
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
                try:
                    final_level_predikaadid.sort(reverse=True)
                except Exception as e:
                    print(e)
                node_count = 0
                for node in nodes:
                    node_obj = Tree_Visualize.objects_by_id(node)
                    if (isinstance(node_obj.predikaadid, dict)):
                        labels = []
                        for key_name in final_level_predikaadid:
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
                                labels[-1] = str(key_name) + ": " + labels[-1]
                            if labeldict[id(node_obj)][1]:
                                labels[-1] = labels[-1] + " :" + str(key_name)
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
    @staticmethod
    def get_predikaadid(vertex, add_param_names):  # My CHANGED FUNCTION
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



if __name__ == '__main__':
    v1_1_1 = Tipp(["9", "7", "M", "M", "L"], [], [])
    v_pikk2 = Tipp(["l", "l", "l", "l", "3"], [], [])
    v_pikk1 = Tipp(["l", "l", "l", "l", "3"], [], [])
    v1_1 = Tipp(["1", "5", "8", "2"], [v1_1_1, v_pikk1], [])
    v1_2 = Tipp(["9", "A", "9", "7"], [], [])
    v1_3_1 = Tipp(["0", "0", "0", "1", "5"], [], [])
    v1_3_2 = Tipp(["0", "0", "0", "2", "5"], [], [])
    v1_3_3_0 = Tipp([True,True,False,True,False], [], [])
    v1_3_3_1 = Tipp([True,True,False,False,False], [], [])
    v1_3_3_2 = Tipp([True,False,False,True,False], [], [])
    v1_3_3 = Tipp(["0", "0", "0", "3", "5"], [v1_3_3_0], [v1_3_3_1,v1_3_3_2])
    v1_3_4 = Tipp(["0", "0", "0", "4", "5"], [], [])
    v1_3_5 = Tipp(["0", "0", "0", "5", "5"], [], [])
    v1_3_6 = Tipp(["0", "0", "0", "6", "5"], [], [])
    v1_3_7 = Tipp(["0", "0", "0", "7", "5"], [], [])
    v1_3_p0 = Tipp(["P", "0", "0", "0", "5"], [], [])
    v1_3_p1 = Tipp(["P", "0", "0", "1", "5"], [], [])
    v1_3_p2 = Tipp(["P", "0", "0", "2", "5"], [], [])
    v1_3_p3 = Tipp(["P", "0", "0", "3", "5"], [], [])
    v1_3_p4 = Tipp(["P", "0", "0", "4", "5"], [], [])
    v1_3 = Tipp(["0", "0", "H", "7"], [v1_3_p0, v1_3_p1, v1_3_p2, v1_3_p3, v1_3_p4],
                  [v1_3_1, v1_3_2, v1_3_3, v1_3_4, v1_3_5, v1_3_6, v1_3_7])
    v1_4_1 = Tipp(["R", "7", "8", "9", "9"], [], [])
    v1_4 = Tipp(["1", "2", "F", "5"], [], [v1_4_1])
    v1 = Tipp(["0", "3", "5"], [v1_1, v1_2, v1_3], [v1_4])
    app = Tree_Visualize(v1)
    print(1)

    v7 = Tipp(["7"], [], [])
    v6 = Tipp(["6"], [v7], [])
    v5 = Tipp(["5"], [], [v6])
    v4 = Tipp(["4"], [v5], [])
    v3 = Tipp({"p1":"3"}, [v4], [])
    v2 = Tipp(["2"], [v3], [])
    v1 = Tipp(["1"], [v2], [])
    v0 = Tipp(["0"], [v1], [])
    app = Tree_Visualize(v0)
    print(2)

    v2 = Tipp({"PARAM1": "A"}, [], [])
    v1 = Tipp({"PARAM1": "B"}, [v2], [])
    v0 = Tipp({"PARAM1": "A"}, [], [v1])
    app = Tree_Visualize(v0)
    print(3)

    v1_1 = Tipp({"PARAM1": "A", "PARAM2": "B", "PARAM3": "C"}, [], [])
    v1_2 = Tipp({"PARAM1": "D", "PARAM3": "E"}, [], [])
    v0 = Tipp({}, [], [v1_1, v1_2])
    app = Tree_Visualize(v0)
    print(4)

    v1_1_1 = Tipp(["9", "7", "M", "M", "L"], [], [])
    v1_1 = Tipp(["1", "5", "8", "2"], [v1_1_1], [])
    v1_2 = Tipp(["9", "A", "9", "7"], [], [])
    v1_3 = Tipp(["0", "0", "H", "7"], [], [])
    v1_5 = Tipp({"PARAM1": "2", "MY_PARAM": "3"}, [], [])
    v1_4_1 = Tipp(["R", "7", "8", "9", "9"], [v1_5], [])
    v1_4 = Tipp(["1", "2", "F", "5"], [], [v1_4_1])
    v1 = Tipp(["0", "3", "5"], [v1_1, v1_2, v1_3], [v1_4])
    app = Tree_Visualize(v1)
    print(5)


    class Something:
        def __init__(self, s):
            self.s = s
        def __eq__(self, other):
            return self.s == other.s
        def __lt__(self, other):
            return self.s < other.s
        def __hash__(self):
            return hash(self.s)
    s1 = Something(1)
    s2 = Something(1)
    S1 = Something(2)
    S2 = Something(2)
    v0_1_1 = Tipp({None: "9"}, [], [])
    v0_1 = Tipp({s1: "1", S1: "2"}, [v0_1_1], [])
    v0_2 = Tipp({s1: "3", S2: "4"}, [], [])
    v0_3_1 = Tipp({None: "N"}, [], [])
    v0_3_2 = Tipp({True: "T"}, [], [])
    v0_3_p0 = Tipp({None: "n", True: "t"}, [], [])
    v0_3_p1 = Tipp({None: "n", False: "f"}, [], [])
    v0_3 = Tipp({s2: "5", S2: "6"}, [v0_3_p0, v0_3_p1], [v0_3_1, v0_3_2])
    v0_4 = Tipp({s2: "7", S1: "9"}, [], [v1_4_1])
    v0 = Tipp({}, [v0_1, v0_2, v0_3], [v0_4])
    app = Tree_Visualize(v0)
    print(6)