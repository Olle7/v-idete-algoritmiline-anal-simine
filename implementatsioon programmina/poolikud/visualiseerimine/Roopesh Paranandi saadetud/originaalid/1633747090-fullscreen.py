import tkinter as tk
import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys

class Vertex:
    def __init__(self, params, type1_branches, type2_branches):
        self.params = params
        self.type1_branches = type1_branches
        self.type2_branches = type2_branches

def get_params(vertex):
    if(isinstance(vertex.predikaadid, list)):
        return(','.join(vertex.predikaadid))

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
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
    def __init__(self,vertices):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.vertices = vertices
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
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i].eitatud_EKd)):
                G.add_edge(get_params(self.vertices[i]), get_params(self.vertices[i].eitatud_EKd[j]))
        type2_edge_labels={}
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i].EKd)):
                G.add_edge(get_params(self.vertices[i]), get_params(self.vertices[i].EKd[j]))
                type2_edge_labels[(get_params(self.vertices[i]),get_params(self.vertices[i].EKd[j]))]= 'x'

        pos = hierarchy_pos(G, get_params(self.vertices[0]))
        nx.draw(G, pos=pos, node_size=4000, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=type2_edge_labels, font_color='red')
        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both',
                                    expand=1)  # `side='top', fill='both', expand=1` will resize plot when you resize window
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand=1)


if __name__ == '__main__':
    v1_1_1 = Vertex(["9", "7", "M", "M", "L"], [], [])
    v1_1 = Vertex(["1", "5", "8", "2"], [v1_1_1], [])
    v1_2 = Vertex(["9", "A", "9", "7"], [], [])
    v1_3 = Vertex(["0", "0", "H", "7"], [], [])
    v1_4_1 = Vertex(["R", "7", "8", "9", "9"], [], [])
    v1_4 = Vertex(["1", "2", "F", "5"], [], [v1_4_1])
    v1 = Vertex(["0", "3", "5"], [v1_1, v1_2, v1_3], [v1_4])
    vertices=[v1_1_1,v1_1,v1_2,v1_3,v1_4_1,v1_4,v1]
    app = Tree_Visualize(vertices)