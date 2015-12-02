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


def asp_and_cc_vs_p():
    asp_and_cc_vs_p_dict = dict()
    average_shortest_path_length = []
    clustering_coefficient = []
    probability = []

    n_nodes = 10

    while True:
        er = 0.3

        while True:
            prob = ((1 + er) * np.log(n_nodes)) / n_nodes

            ws_graph = generate_ws_graph(n_nodes, prob)

            if nx.is_connected(ws_graph):
                print('Graph IS connected!')
                # graph_utils.draw_graph(ws_graph)

                break
            else:
                print('Graph IS NOT connected!')

                er += 0.01

        avg_shortest_path = nx.average_shortest_path_length(ws_graph)
        average_shortest_path_length.append(float("{0:.2f}".format(avg_shortest_path)))
        print 'avg. shortest path length: ' + str(float("{0:.2f}".format(avg_shortest_path)))

        probability.append(prob)
        print 'probability: ' + str(prob)

        cc = 0 # Aqui hay que calcular el clustering coefficient
        clustering_coefficient.append(cc)
        print 'clustering coefficient: ' + str(cc)

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

    asp_and_cc_vs_p_dict['probability'] = probability
    asp_and_cc_vs_p_dict['average_shortest_path_length'] = average_shortest_path_length
    asp_and_cc_vs_p_dict['clustering_coefficient'] = clustering_coefficient

    return asp_and_cc_vs_p_dict


def main():
    asp_and_cc_vs_p_dict = asp_and_cc_vs_p()

    print asp_and_cc_vs_p_dict

    # Aqui normalizas los arreglos y ploteas


main()