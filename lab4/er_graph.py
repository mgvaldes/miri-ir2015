from networkx.algorithms.isolate import is_isolate

__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import random
import numpy as np
import graph_utils


def generate_er_graph(n_nodes, prob):
    # Creating undirected graph
    er_graph = nx.Graph()

    # Adding n_nodes to graph
    for i in range(n_nodes):
        er_graph.add_node(i)

    # Adding edges between all pair of nodes with probability prob
    for i in range(n_nodes):
        for j in range(i, n_nodes):
            rand_prob = random.random()

            if rand_prob < prob:
                er_graph.add_edge(i, j)

    return er_graph


def main():
    n_nodes = 10

    er = 0
    prob = ((1 + er) * np.log(n_nodes)) / n_nodes

    while prob < 1.0:
        er_graph = generate_er_graph(n_nodes, prob)

        if not graph_utils.has_isolated_node(er_graph):
            print('Graph IS connected!')
            graph_utils.draw_graph(er_graph)

            break
        else:
            print('Graph IS NOT connected!')

            prob += 0.01


main()