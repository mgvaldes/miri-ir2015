__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(g):
    nx.draw(g)
    plt.show()


def has_isolated_node(g):
    for node in g.nodes():
        if nx.is_isolate(g, node):
            return True

    return False