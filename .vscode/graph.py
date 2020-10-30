from graphviz import Graph

worldMap = Graph()
with worldMap.subgraph(name='cluster0') as c:
    #c.node('A')
    #c.node('B')
    c.edge('A','B')
with worldMap.subgraph(name='cluster1') as c:
    c.node('L')
    c.node('C')


#worldMap.edges(['AB', 'AL'])
#dot.edge('B', 'L')
worldMap.edge('A', 'C')


#worldMap.node('A','TEST')
#worldMap.render()  
dot.view()