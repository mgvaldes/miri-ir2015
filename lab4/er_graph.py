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


def average_shortest_path_length_vs_network_size():
    average_shortest_path_length_vs_network_size_dict = dict()
    average_shortest_path_length = []
    network_size = []

    n_nodes = 50

    while True:
        er = 0.25

        while True:
            prob = ((1 + er) * np.log(n_nodes)) / n_nodes

            er_graph = generate_er_graph(n_nodes, prob)

            if nx.is_connected(er_graph):
                # Graph IS connected
                break
            else:
                # Graph IS NOT connected
                er += 0.01

        avg_shortest_path = nx.average_shortest_path_length(er_graph)

        network_size.append(n_nodes)
        print '# of nodes: ' + str(n_nodes)

        average_shortest_path_length.append(float("{0:.2f}".format(avg_shortest_path)))
        print 'avg. shortest path length: ' + str(float("{0:.2f}".format(avg_shortest_path)))

        # if 10 <= n_nodes < 100:
        #     n_nodes += 10
        if 50 <= n_nodes < 1000:
            n_nodes += 50
        elif 1000 <= n_nodes < 3000:
            n_nodes += 100
        elif 3000 <= n_nodes < 7000:
            n_nodes += 250
        elif 7000 <= n_nodes < 12000:
            n_nodes += 500
        else:
            break

    average_shortest_path_length_vs_network_size_dict['network_size'] = network_size
    average_shortest_path_length_vs_network_size_dict['average_shortest_path_length'] = average_shortest_path_length

    return average_shortest_path_length_vs_network_size_dict


def main():
    average_shortest_path_length_vs_network_size_dict = average_shortest_path_length_vs_network_size()

    print average_shortest_path_length_vs_network_size_dict

    graph_utils.plot_avg_shortest_path_length_vs_nodes(average_shortest_path_length_vs_network_size_dict['average_shortest_path_length'], average_shortest_path_length_vs_network_size_dict['network_size'])


main()