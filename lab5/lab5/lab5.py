__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'

import csv
from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance


def create_graph_from_file():
    g = nx.Graph()

    with open('/Users/gaby/Documents/MIRI/3rd_Semester/IR/miri-ir2015/lab5/cosine_similarities.txt', 'rb') as csv_file:
    # with open('/home/jose/Projects/IR/lab5/cosine_similarities.txt', 'rb') as csv_file:
        # for row in f_reader:
        for row in csv.reader(csv_file.read().splitlines(), delimiter=';'):
            if float(row[2]) > 0.2:
                g.add_edge(row[0].split(".")[0], row[1].split(".")[0])

    con_comp = list(nx.connected_components(g))
    con_comp.sort(key=len, reverse=True)

    connected_comp_graphs = list(nx.connected_component_subgraphs(g, copy=True))
    connected_comp_graphs.sort(key=lambda gr: gr.number_of_nodes(), reverse=True)

    new_connected_graph = connected_comp_graphs[0]

    print("Number of nodes: " + str(new_connected_graph.number_of_nodes()))
    print("Number of edges: " + str(new_connected_graph.number_of_edges()))
    print("Number of connected components: " + str(nx.number_connected_components(new_connected_graph)))
    print("Is connected?: " + str(nx.is_connected(new_connected_graph)))
    print("Nodes: " + str(new_connected_graph.nodes()))

    return new_connected_graph


def create_hc(G):
    """Creates hierarchical cluster of graph G from distance matrix"""
    path_length = nx.all_pairs_shortest_path_length(G)
    distances = numpy.zeros((len(G), len(G)))

    l1 = sorted(path_length.items(), key=lambda x: x[0])

    for u, p in l1:
        l2 = sorted(p.items(), key=lambda x: x[0])

        for v, d in l2:
            x = get_index_of_tuple(l1, 0, u)
            y = get_index_of_tuple(l2, 0, v)
            distances[x][y] = d

    # Create hierarchical cluster
    Y = distance.squareform(distances)
    Z = hierarchy.complete(Y)  # Creates HC using farthest point linkage

    # This partition selection is arbitrary, for illustrive purposes
    membership = list(hierarchy.fcluster(Z, t=1.15))

    # Create collection of lists for blockmodel
    partition = defaultdict(list)

    for n, p in zip(list(range(len(G))), membership):
        partition[p].append(n)

    # [0, 179, 305]
    # print "Clustering [0, 179, 305]"
    # print l1[0][0], l1[179][0], l1[305][0]

    return list(partition.values())


def get_index_of_tuple(l, index, value):
    for pos, t in enumerate(l):
        if t[index] == value:
            return pos

    # Matches behavior of list.index
    raise ValueError("list.index(x): x not in list")


def cluster_to_file(cluster_list, cluster_id):
    cluster_file = open('../hc_clusters_clean/cluster' + str(cluster_id) + ".txt", 'w')

    for elem in cluster_list:
        try:
            tweet_file = open('../clean_tweets/tweet' + str(elem) + '.txt')
            cluster_file.write(tweet_file.read() + '\n')
        except IOError:
            continue


def main():
    g = create_graph_from_file()

    hc_clusters = create_hc(g)

    for i in range(0, len(hc_clusters)-1):
        cluster_to_file(hc_clusters[i], i)

    print hc_clusters

main()