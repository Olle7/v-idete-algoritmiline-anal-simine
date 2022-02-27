import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
from collections import deque

class Vertex:
    def __init__(self, params, type1_branches, type2_branches):
        self.params = params
        self.type1_branches = type1_branches
        self.type2_branches = type2_branches

def get_params(vertex):
    if(isinstance(vertex.predikaadid, list)):
        return('\n'.join(vertex.predikaadid))
    elif(isinstance(vertex.predikaadid, dict)):
        return('\n'.join(vertex.predikaadid.values()))

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
        while(dq):
            vert = dq.pop()
            for j in range(len(vert.eitatud_EKd)):
                G.add_edge(get_params(vert), get_params(vert.eitatud_EKd[j]))
                dq.appendleft(vert.eitatud_EKd[j])
            for k in range(len(vert.EKd)):
                G.add_edge(get_params(vert), get_params(vert.EKd[k]))
                type2_edge_labels[(get_params(vert), get_params(vert.EKd[k]))] = 'x'
                dq.appendleft(vert.EKd[k])

        pos = hierarchy_pos(G, get_params(self.root_vertex))
        flipped_pos = {node: (x, -y) for (node, (x, y)) in pos.items()}
        nx.draw(G, pos=flipped_pos,font_size=7, node_size=1800, node_color='white', with_labels=True)
        nx.draw_networkx_edge_labels(G, flipped_pos, edge_labels=type2_edge_labels, font_color='red')
        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both',
                                    expand=1)  # `side='top', fill='both', expand=1` will resize plot when you resize window
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand=1)


if __name__ == '__main__':
    v1_1_1 = Vertex(["9", "7", "M", "M", "L"], [], [])
    v_pikk2 = Vertex(["l", "l", "l", "l", "3"], [], [])
    v_pikk1 = Vertex(["l", "l", "l", "l", "3"], [], [])
    v1_1 = Vertex(["1", "5", "8", "2"], [v1_1_1, v_pikk1], [])
    v1_2 = Vertex(["9", "A", "9", "7"], [], [])
    v1_3_1 = Vertex(["0", "0", "0", "1", "5"], [], [])
    v1_3_2 = Vertex(["0", "0", "0", "2", "5"], [], [])
    v1_3_3 = Vertex(["0", "0", "0", "3", "5"], [], [])
    v1_3_4 = Vertex(["0", "0", "0", "4", "5"], [], [])
    v1_3_5 = Vertex(["0", "0", "0", "5", "5"], [], [])
    v1_3_6 = Vertex(["0", "0", "0", "6", "5"], [], [])
    v1_3_7 = Vertex(["0", "0", "0", "7", "5"], [], [])
    v1_3_p0 = Vertex(["P", "0", "0", "0", "5"], [], [])
    v1_3_p1 = Vertex(["P", "0", "0", "1", "5"], [], [])
    v1_3_p2 = Vertex(["P", "0", "0", "2", "5"], [], [])
    v1_3_p3 = Vertex(["P", "0", "0", "3", "5"], [], [])
    v1_3_p4 = Vertex(["P", "0", "0", "4", "5"], [], [])
    v1_3 = Vertex(["0", "0", "H", "7"], [v1_3_p0, v1_3_p1, v1_3_p2, v1_3_p3, v1_3_p4],
                  [v1_3_1, v1_3_2, v1_3_3, v1_3_4, v1_3_5, v1_3_6, v1_3_7])
    v1_4_1 = Vertex(["R", "7", "8", "9", "9"], [], [])
    v1_4 = Vertex(["1", "2", "F", "5"], [], [v1_4_1])
    v1 = Vertex(["0", "3", "5"], [v1_1, v1_2, v1_3], [v1_4])
    # app = Tree_Visualize(v1)
    print(1)

    v7 = Vertex(["7"], [], [])
    v6 = Vertex(["6"], [v7], [])
    v5 = Vertex(["5"], [], [v6])
    v4 = Vertex(["4"], [v5], [])
    v3 = Vertex(["3"], [v4], [])
    v2 = Vertex(["2"], [v3], [])
    v1 = Vertex(["1"], [v2], [])
    v0 = Vertex(["0"], [v1, v7], [])
    # app = Tree_Visualize(v0)
    print(2)

    v2 = Vertex({"PARAM1": "A"}, [], [])
    v1 = Vertex({"PARAM1": "B"}, [v2], [])
    v0 = Vertex({"PARAM1": "A"}, [], [v1])
    #app = Tree_Visualize(v0)
    print(2)

    v1_1 = Vertex({"PARAM1": "A","PARAM2": "B","PARAM3": "C"}, [], [])
    v1_2 = Vertex({"PARAM1": "D", "PARAM3": "E"}, [], [])
    v0 = Vertex({}, [], [v1_1,v1_2])
    app = Tree_Visualize(v0)
    print(2)