__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'

import csv
from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance
from matplotlib import pyplot as plt


def create_graph_from_file():
    g = nx.Graph()

    # with open('/Users/gaby/Documents/MIRI/3rd_Semester/IR/Lab5/cosine_similarities.txt', 'rb') as csv_file:
    with open('/home/jose/Projects/IR/lab5/cosine_similarities.txt', 'rb') as csv_file:
        # for row in f_reader:
        for row in csv.reader(csv_file.read().splitlines(), delimiter=';'):
            if float(row[2]) > 0.2:
                g.add_edge(row[0].split(".")[0], row[1].split(".")[0])

    con_comp = list(nx.connected_components(g))
    con_comp.sort(key=len, reverse=True)

    connected_comp_graphs = list(nx.connected_component_subgraphs(g, copy=True))
    connected_comp_graphs.sort(key=lambda gr: gr.number_of_nodes(), reverse=True)

    new_connected_graph = connected_comp_graphs[0]

    # print("Number of nodes: " + str(new_connected_graph.number_of_nodes()))
    # print("Number of edges: " + str(new_connected_graph.number_of_edges()))
    # print("Number of connected components: " + str(nx.number_connected_components(new_connected_graph)))
    # print("Is connected?: " + str(nx.is_connected(new_connected_graph)))
    # print("Nodes: " + str(new_connected_graph.nodes()))

    return new_connected_graph


def create_hc(G):
    """Creates hierarchical cluster of graph G from distance matrix"""
    path_length = nx.all_pairs_shortest_path_length(G)
    distances = numpy.zeros((len(G), len(G)))

    # l1 = sorted(path_length.items(),key=lambda x: x[0])
    # for u, p in l1:
    #     l2 = sorted(p.items(),key=lambda x: x[0])
    #     for v, d in l2:
    #         x = getIndexOfTuple(l1, 0, u)
    #         y = getIndexOfTuple(l2, 0, v)
    #         distances[x][y] = d
    for u,p in path_length.items():
        for v,d in p.items():
            distances[u][v]=d


    # Create hierarchical cluster
    Y = distance.squareform(distances)
    Z = hierarchy.complete(Y)  # Creates HC using farthest point linkage

    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    hierarchy.dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()

    # This partition selection is arbitrary, for illustrive purposes
    membership = list(hierarchy.fcluster(Z, t=1.15))

    # Create collection of lists for blockmodel
    partition = defaultdict(list)

    for n, p in zip(list(range(len(G))), membership):
        partition[p].append(n)

    return list(partition.values())


def get_index_of_tuple(l, index, value):
    for pos, t in enumerate(l):
        if t[index] == value:
            return pos

    # Matches behavior of list.index
    raise ValueError("list.index(x): x not in list")


def cluster_to_file(cluster_list, cluster_id):
    cluster_file = open('../hc_clusters/cluster' + str(cluster_id) + ".txt", 'w')

    for elem in cluster_list:
        tweet_file = open('../tweets/tweet' + str(elem) + '.txt')
        cluster_file.write(tweet_file.read() + '\n')


def girvan_newman(G):
    """ run the algorithm of Girvan + Newman up to the first separation
        return: list of components of G, list of edges removed
    """

    # we're going to remove edges, so do it on a copy of the original graph
    G = G.copy()

    def find_best_edge(G0):
        """ get the edge from G0 with highest betweenness centrality"""
        eb = nx.edge_betweenness_centrality(G0)
        edges = eb.keys()
        return max(edges, key=lambda e: eb[e])

    removed_edges = []
    # Proceed until we separate the graph
    while nx.number_connected_components(G) == 1:
        u, v = find_best_edge(G)
        G.remove_edge(u, v)
        removed_edges.append((u, v))

    return list(nx.connected_components(G)), removed_edges


def main():
    g = create_graph_from_file()

    H=nx.convert_node_labels_to_integers(g)

    hc_clusters = create_hc(H)

    # gn = girvan_newman(H)

    # cliques = nx.find_cliques(H)
    # clique = nx.k_clique_communities(H,cliques)

    for i in range(0, len(hc_clusters)-1):
        cluster_to_file(hc_clusters[i], i)

    print hc_clusters

main()