import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
from collections import deque
import gc

class Vertex:
    def __init__(self, params, type1_branches, type2_branches):
        self.params = params
        self.type1_branches = type1_branches
        self.type2_branches = type2_branches

def get_params(vertex):
    if(isinstance(vertex.params,list)):
        return('\n'.join(vertex.params))
    elif(isinstance(vertex.params,dict)):
        final_list = []
        final_list=vertex.params.values()

        return('\n'.join(final_list))

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
        level_params=[]
        nodes = set(nx.ego_graph(G, id(root), radius=count))
        nodes -= set(nx.ego_graph(G, id(root), radius=count-1))
        nodes=list(nodes)
        if len(nodes) == 0:
            break
        else:
            for node in nodes:
                node_obj = objects_by_id(node)
                if (isinstance(node_obj.params,dict)):
                    level_nodes.append(node_obj)
                    level_params.extend(node_obj.params.keys())
            level_params=list(set(level_params))
            final_level_params=[]
            for param in level_params:
                match=False
                for param1 in final_level_params:
                    try:
                        print(param,param1)
                        if param==param1:
                            match=True
                    except Exception as e:
                        print(e)
                if match==False:
                    final_level_params.append(param)
            try:
                final_level_params.sort()
            except Exception as e:
                print(e)
            node_count=0
            for node in nodes:
                node_obj = objects_by_id(node)
                if(isinstance(node_obj.params,dict)):
                    labels=[]
                    for key_name in final_level_params:
                        if key_name in node_obj.params.keys():
                            labels.append(node_obj.params[key_name])
                        else:
                            keycount = 0
                            for keyvalue in node_obj.params.keys():
                                if keyvalue==key_name:
                                    labels.append(node_obj.params[keyvalue])
                                    keycount=keycount+1
                            if(keycount==0):
                                labels.append(" ")
                                print("Added")
                    if node_count==0:
                        labeldict[id(node_obj)]='\n'.join(labels)
                    else:
                        labeldict[id(node_obj)]='\n'.join(labels)
                    node_count+=1
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
        a = f.add_subplot(111)
        G = nx.Graph()
        dq = deque([self.root_vertex])
        type2_edge_labels = {}
        labeldict={}
        while(dq):
            vert = dq.pop()
            labeldict[id(vert)]=get_params(vert)
            for j in range(len(vert.type1_branches)):
                G.add_edge(id(vert),id(vert.type1_branches[j]))
                dq.appendleft(vert.type1_branches[j])
            for k in range(len(vert.type2_branches)):
                G.add_edge(id(vert),id(vert.type2_branches[k]))
                type2_edge_labels[id(vert), id(vert.type2_branches[k])] = 'x'
                dq.appendleft(vert.type2_branches[k])
        fill_the_gaps_of_the_param_tree(G,self.root_vertex,labeldict)
        pos = hierarchy_pos(G, id(self.root_vertex))
        flipped_pos = {node: (x, -y) for (node, (x, y)) in pos.items()}
        nx.draw(G, pos=flipped_pos,font_size=7, node_size=1800, node_color='white',labels=labeldict, with_labels=True)
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

   def __hash__(self):
       return hash(self.s)

   def __lt__(self, other):
       return self.s < other.s

if __name__ == '__main__':
    v0_0 = Vertex({1: "0:1", 5: "0:5", 6: "0:6"}, [], [])
    v0_1 = Vertex({1: "1", 2: "2", 4: "4", 5: "5", 6: "6"}, [], [])
    v0_2 = Vertex({1: "1", 7: "7"}, [], [])
    v0_3 = Vertex({0: "0", 5: "3:5"}, [], [])
    v0_4 = Vertex(["R", "T", "Y"], [], [])
    v0 = Vertex({"W": "w", "R": "r"}, [v0_1, v0_2, v0_3, v0_4], [v0_0])
    #app = Tree_Visualize(v0)
    if True:
        v0_0 = Vertex(["1","2"], [], [])
        v0_1 = Vertex(["A","B","C","D","E","F"], [], [])
        v0_2 = Vertex(["a","b","c"], [], [])
        v0 = Vertex(["r"],[v0_1, v0_2],[v0_0])
        app = Tree_Visualize(v0)