__author__ = 'zac'
from Parser import Parser
import networkx as nx
import matplotlib.pylab as plt
class Graphistory:
    def __init__(self,historyFile):
        self.data = []
        self.parser = Parser(historyFile)
        (self.fromGraph, self.toGraph) = self.parser .graphmaker()
    def draw_from_site(self, site_name, number_of_node =10, radius =100):
        self._draw_single(self.fromGraph, site_name, number_of_node)

    def draw_to_site(self, site_name, number_of_node =10, radius =100):
        self._draw_single(self.toGraph, site_name, number_of_node)

    #return a graph( set of edges to be more precise) with only
    # 'n' nodes
    def _filter(self, edges, n):
        #sort edges according to weight
        edges = sorted(edges, key = lambda tmp:tmp[2]['weight'], reverse = True)
        return edges[0: n - 1]

    def _draw_single(self, DG, site, number_of_node = 10, multiplier = 100):
        if not site in DG:
            raise Exception("site doesn't exist")
        # turn into s single graph
        edges = DG.edges(site, data = True)
        #sort the edges according to weight
        edges = self._filter(edges, number_of_node )

                ##filter out low weighted edge
                #to_delete = list()
                #if len(edges) > 15 :
                #    for (a) in edges:
                #        if a[2]['weight'] < 10 :
                #            to_delete.append(a)
                #    for item in to_delete:
                #        edges.remove(item)
                # print edges
        #turn into single graph with node 'site' as the center(call it main node)
        tmpGraph = nx.Graph()
        tmpGraph.add_edges_from(edges)
        # print tmpGraph.edges(data = True)
        pos=nx.graphviz_layout(tmpGraph)
        edgewidth = []

        max = 0
        radius =[]
        max_weight = 0
        main_node_index = 0
        #set the size for each node
        for node in tmpGraph.nodes():
            if node==site:
                #remember index of main node
                #since we want the main node to be the biggest
                main_node_index = len(radius)
                radius.append(1) #dummy value
            else:

                weight =  tmpGraph[site][node]['weight'] * multiplier
                if weight > max_weight:
                    max_weight =weight
                # weight = tmpGraph.edge([node,site])['weight']
                radius.append(weight)

         #make sure radius of main node is always the biggest
        radius[main_node_index] = max_weight * 1.5

        #big nodes come big edges
        for (u,v,d) in tmpGraph.edges(data=True):
            edgewidth.append(d['weight'])

        edge_labels=dict([((u,v,),d['weight'])
            for u,v,d in tmpGraph.edges(data=True)])
        # nx.draw_networkx_edges(tmpGraph,pos,alpha=0.3,width=edgewidth, edge_color='m')
        nx.draw_networkx_edges(tmpGraph,pos,alpha=0.3, width=10,edge_color='m')
        nx.draw_networkx_nodes(tmpGraph,pos,node_color='w',node_size = radius*100,alpha=0.4)
        nx.draw_networkx_labels(tmpGraph,pos,fontsize=14)
        #nx.draw_networkx_edge_labels(tmpGraph, pos)
        nx.draw_networkx_edge_labels(tmpGraph,pos,edge_labels=edge_labels)

        plt.show()


