__author__ = 'zac'
from Parser import Parser
import networkx as nx
import matplotlib.pylab as plt
class Graphistory:
    def __init__(self,historyFile):
        self.data = []
        self.parser = Parser(historyFile)
        (self.fromGraph, self.toGraph) = self.parser .graphmaker()
    def draw_from_site(self, site_name):
        self.draw_single(self.fromGraph, site_name)

    def draw_to_site(self, site_name):
        self.draw_single(self.toGraph, site_name)

    def draw_single(self, DG, site, multiplier = 100):
        if not site in DG:
            raise Exception("site doesn't exist")
        # turn into s single graph
        edges = DG.edges(site, data = True)
        # print edges
        tmpGraph = nx.Graph()
        tmpGraph.add_edges_from(edges)
        # print tmpGraph.edges(data = True)
        pos=nx.graphviz_layout(tmpGraph)
        edgewidth = []

        max = 0
        radius =[]
        max_weight = 0
        main_node_index = 0
        for node in tmpGraph.nodes():
            if node==site:
                main_node_index = len(radius)
                radius.append(1)
            else:

                weight =  tmpGraph[site][node]['weight'] * multiplier
                if weight > max_weight:
                    max_weight =weight
                # weight = tmpGraph.edge([node,site])['weight']
                radius.append(weight)
         #make sure radius of main node is always the biggest
        radius[main_node_index] = max_weight * 1.5
        for (u,v,d) in tmpGraph.edges(data=True):
            edgewidth.append(d['weight'])
        # nx.draw_networkx_edges(tmpGraph,pos,alpha=0.3,width=edgewidth, edge_color='m')
        nx.draw_networkx_edges(tmpGraph,pos,alpha=0.3, width=10,edge_color='m')
        nx.draw_networkx_nodes(tmpGraph,pos,node_color='w',node_size = radius*100,alpha=0.4)
        nx.draw_networkx_labels(tmpGraph,pos,fontsize=14)
        plt.show()


