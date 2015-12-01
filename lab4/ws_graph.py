__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import random
import numpy as np
import graph_utils


def generate_ws_graph(n_nodes, prob):
    # Creating undirected graph
    ws_graph = nx.Graph()

    # Adding n_nodes to graph
    for i in range(n_nodes):
        ws_graph.add_node(i)

    # Adding edges from each node to it's 4 closest nodes
    for i in range(n_nodes):
        ws_graph.add_edge(i, (i + 1) % 10)
        ws_graph.add_edge(i, (i + 2) % 10)

    for edge in ws_graph.edges():
        origin_node = edge[0]
        random_node = random.randint(0, n_nodes - 1)

        rand_prob = random.random()

        if rand_prob < prob:
            ws_graph.remove_edge(*edge)
            ws_graph.add_edge(origin_node, random_node)

    return ws_graph


def main():
    n_nodes = 10

    er = 0
    prob = ((1 + er) * np.log(n_nodes)) / n_nodes

    while prob < 1.0:
        er_graph = generate_ws_graph(n_nodes, prob)

        if not graph_utils.has_isolated_node(er_graph):
            print('Graph IS connected!')
            graph_utils.draw_graph(er_graph)

            break
        else:
            print('Graph IS NOT connected!')

            prob += 0.01

main()