from networkx.algorithms.isolate import is_isolate

__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import random
import numpy as np
from time import time
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

    n_nodes = 10

    while True:
        # start = time()

        er = 0.3

        while True:
            prob = ((1 + er) * np.log(n_nodes)) / n_nodes

            er_graph = generate_er_graph(n_nodes, prob)

            if nx.is_connected(er_graph):
                print('Graph IS connected!')
                # graph_utils.draw_graph(er_graph)

                break
            else:
                print('Graph IS NOT connected!')

                er += 0.01

        # elapsed = time() - start
        # print("done in %.3fs" % elapsed)
        #
        # if elapsed > 120:
        #     break

        network_size.append(n_nodes)
        print '# of nodes: ' + str(n_nodes)

        avg_shortest_path = nx.average_shortest_path_length(er_graph)
        average_shortest_path_length.append(avg_shortest_path)
        print 'avg. shortest path length: ' + str(avg_shortest_path)

        if 10 <= n_nodes < 100:
            n_nodes += 10
        elif 100 <= n_nodes < 1000:
            n_nodes += 100
        elif 1000 <= n_nodes < 3000:
            n_nodes += 200
        elif 3000 <= n_nodes < 8000:
            n_nodes += 500
        else:
            break

    average_shortest_path_length_vs_network_size_dict['network_size'] = network_size
    average_shortest_path_length_vs_network_size_dict['average_shortest_path_length'] = average_shortest_path_length

    return average_shortest_path_length_vs_network_size_dict


def main():
    average_shortest_path_length_vs_network_size_dict = average_shortest_path_length_vs_network_size()

    print average_shortest_path_length_vs_network_size_dict
    # average_shortest_path_length_vs_network_size_dict = {'network_size': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000], 'average_shortest_path_length': [2.1333333333333333, 2.5473684210526315, 2.52183908045977, 2.567948717948718, 2.5787755102040815, 2.7994350282485874, 2.718840579710145, 2.7835443037974685, 2.8666666666666667, 2.857979797979798, 2.970251256281407, 3.103076923076923, 3.218671679197995, 3.3185490981963928, 3.323861992209238, 3.3763662374821175, 3.3798185231539426, 3.4372413793103447, 3.4824664664664664, 3.499660828468168, 3.5144940263453486, 3.57848655409631, 3.6228799950589834, 3.627856928464232, 3.6841175741039316, 3.6783333333333332, 3.6863343889661704, 3.71246695248303, 3.7390450150050016, 3.7740449924468216, 3.800299824956239, 3.820426959077326, 3.868561472294459, 3.8698007902263223, 3.9049546035450353, 3.913364564962657, 3.9266689118853715, 3.946520193803618, 3.9776068571071383]}

    graph_utils.plot_avg_shortest_path_length_vs_nodes(average_shortest_path_length_vs_network_size_dict['average_shortest_path_length'], average_shortest_path_length_vs_network_size_dict['network_size'])


main()