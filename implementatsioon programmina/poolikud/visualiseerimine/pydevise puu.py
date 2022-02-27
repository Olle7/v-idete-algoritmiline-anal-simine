from pyvis import network as net
from IPython.core.display import display, HTML
g=net.Network(height='400px', width='50%',heading='Graph')
g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_edge(1,2)
g.add_edge(2,3)
g.show('example.html')
display(HTML('example.html'))