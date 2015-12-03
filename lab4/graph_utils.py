__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'


import networkx as nx
import matplotlib.pyplot as plt
import pylab


def draw_graph(g):
    nx.draw(g)
    plt.show()


def has_isolated_node(g):
    for node in g.nodes():
        if nx.is_isolate(g, node):
            return True

    return False


def plot_avg_shortest_path_length_vs_nodes(avg_shortest_path_lengths, nodes):
    plt.figure()
    plt.plot(nodes, avg_shortest_path_lengths, 'bo', nodes, avg_shortest_path_lengths, 'k')
    plt.xlabel('num nodes')
    plt.ylabel('average shortest path')
    plt.tight_layout()
    plt.show()

    # pylab.savefig('/Users/gaby/Documents/MIRI/3rd_Semester/IR/miri-ir2015/lab4/avg_shortest_path_length_vs_nodes.png')

def plot_asp_and_cc_vs_p(asp, cc, p):
    plt.figure()
    plt.plot(asp, p, 'bo', linestyle='-')
    plt.plot(cc, p, 'rs', linestyle='-')
    plt.xlabel('p')
    plt.tight_layout()
    plt.show()