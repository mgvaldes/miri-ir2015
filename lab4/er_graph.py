__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np


def generate_er_graph(n_nodes, prob):
    # Creating undirected graph
    er_graph = nx.Graph()

    # Adding n_nodes to graph
    for i in range(n_nodes):
        er_graph.add_node(i)

    # Adding edges between all pair of nodes with probability prob
    for i in range(n_nodes):
        for j in range(i, n_nodes):
            if random.random < prob:
                er_graph.add_edge(i, j)

    return er_graph


def draw_graph(g):
    nx.draw(g)
    plt.show()


def main():
    n_nodes = 10

    er = 0
    prob = ((1 + er) * np.log(n_nodes)) / n_nodes

    while True:
        er_graph = generate_er_graph(n_nodes, prob)

        if nx.connected_components(er_graph)[1]:
            print('Graph IS connected!')

            break
        else:
            print('Graph IS NOT connected!')

            prob += 0.01

    prob = ((1 + er) * np.log(n_nodes)) / n_nodes

    while True:
        ws_graph = generate_er_graph(n_nodes, prob)

        if nx.connected_components(ws_graph)[1]:
            print('Graph IS connected!')

            break
        else:
            print('Graph IS NOT connected!')

            prob += 0.01

    