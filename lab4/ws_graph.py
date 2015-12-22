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
        ws_graph.add_edge(i, (i + 1) % n_nodes)
        ws_graph.add_edge(i, (i + 2) % n_nodes)

    for edge in ws_graph.edges():
        origin_node = edge[0]
        random_node = random.randint(0, n_nodes - 1)

        rand_prob = random.random()

        if rand_prob < prob:
            ws_graph.remove_edge(*edge)
            ws_graph .add_edge(origin_node, random_node)

    return ws_graph


def asp_and_cc_vs_p():
    N_NODES = 1000
    EPSILON = 0.01

    asp_and_cc_vs_p_dict = dict()
    average_shortest_path_length = []
    clustering_coefficient = []
    probability = []

    n_nodes = N_NODES
    prob = 0.0

    c0 = None
    l0 = None

    while prob <= 1:
        ws_graph = nx.connected_watts_strogatz_graph(n_nodes, 4, prob)  # Using networkx for finding the graph


        avg_shortest_path = nx.average_shortest_path_length(ws_graph)
        average_shortest_path_length.append(float("{0:.2f}".format(avg_shortest_path)))  # Store shortest path of the graph
        print 'avg. shortest path length: ' + str(float("{0:.2f}".format(avg_shortest_path)))

        probability.append(prob)  # Store probability
        print 'probability: ' + str(prob)

        cc = nx.average_clustering(ws_graph)
        clustering_coefficient.append(cc)  # Store clustering coefficient
        print 'clustering coefficient: ' + str(cc)

        if prob == 0.0:   #Only first iteration
            c0 = cc
            l0 = float("{0:.2f}".format(avg_shortest_path))


        prob += EPSILON


    asp_and_cc_vs_p_dict['probability'] = probability
    asp_and_cc_vs_p_dict['average_shortest_path_length'] = average_shortest_path_length
    asp_and_cc_vs_p_dict['clustering_coefficient'] = clustering_coefficient

    return asp_and_cc_vs_p_dict, c0, l0


def main():
    asp_and_cc_vs_p_dict, c0, l0 = asp_and_cc_vs_p()

    print asp_and_cc_vs_p_dict

    norm = max(asp_and_cc_vs_p_dict['average_shortest_path_length'])  # Prior try
    norm_asp = [float(x)/l0 for x in asp_and_cc_vs_p_dict['average_shortest_path_length']]

    norm = max(asp_and_cc_vs_p_dict['clustering_coefficient'])  # Prior try
    norm_cc = [float(x)/c0 for x in asp_and_cc_vs_p_dict['clustering_coefficient']]

    norm_p = [x for x in asp_and_cc_vs_p_dict['probability']]  # Actually we are doing nothing

    graph_utils.plot_asp_and_cc_vs_p(norm_asp, norm_cc, norm_p)


main()
