import matplotlib
import scipy
import higra as hg
t = hg.Tree((7, 7, 8, 8, 8, 9, 9, 11, 10, 10, 11, 11))
#hg.plot_graph(t,vertex_positions=[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],[11,11],[12,12]])
hg.plot_partition_tree(t)