import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
import sys
sys.path.append("/Users/mat/Desktop/Xanadu/FlashDrive/src/gbsapps")


adj = np.array(
    [
        [0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1, 0],
    ]
)

graph2 = nx.Graph(adj)

import random

def find_dense_subgraph(graph, nodes=2):
    import gbsapps.graph.dense_subgraph as dense

    print("graph.edges", graph.edges)

    result = dense.find_dense_subgraph(
        graph=graph, number_of_nodes=nodes, iterations=1, method="random-search"
    )

    subgraph = graph.subgraph(result[1])

    # labels = {0: "Quantum", 1: "Toronto", 2: "Ajay Agrawal", 3: "Government", 4: "CDL", 5: "Advantage"}
    # pos = nx.spring_layout(graph, seed=1)
    # nx.draw_networkx_edges(
    #     graph, pos, edgelist=subgraph.edges, width=8, alpha=0.5, edge_color="#ff3300"
    # )
    # nx.draw_networkx_nodes(graph, pos, nodelist=subgraph.nodes, node_size=500, node_color="#ff3300")

    # nx.draw_networkx_nodes(graph, pos, node_color="#63AC9A")
    # nx.draw_networkx_edges(graph, pos, width=2, edge_color="#63AC9A")
    # nx.draw_networkx_labels(graph, pos, labels, font_size=16)

    # l, r = plt.xlim()
    # plt.xlim(l - 0.35, r + 0.35)
    # plt.axis("off")

    density = np.round(result[0], 2)

    print("Density: {}".format(density))

    return subgraph, density

if __name__ == "__main__":
    g = nx.Graph()
    g.add_edge("x", "y", weight=0.4)
    g.add_edge("z", "y", weight=0.4)
    g.add_edge("c", "x", weight=0.0)
    print("dadas", find_dense_subgraph(g))


##############################################################################
# Extensions
# ----------
#
# This tutorial has focused on a relatively simple :math:`6`-node graph. Here, the densest
# :math:`4`-node subgraph is simple to find: a brute force search requires only :math:`15`
# possibilities. To really appreciate the difficulty of the densest-:math:`k` subgraph problem we
# need to increase the size of the graph. Suppose we want to search for the densest
# :math:`10`-node subgraph of a :math:`30`-node graph like the one shown below. There are now
# just over thirty million possibilities!
#
# .. image:: ../_static/graph.png
#     :align: center
#     :width: 50%
#     :alt: Example graph
#
# The densest :math:`10`-node subgraph is highlighted in red. As a challenge, see if you can use
# the tools learned in this tutorial to write a script for finding dense :math:`10`-node
# subgraphs. The graph shown above is available as an `adjacency matrix
# <https://en.wikipedia.org/wiki/Adjacency_matrix>`__ in CSV format :download:`here
# <../_static/graph.csv>`.
#
# .. warning::
#
#    Through `Strawberry Fields <https://strawberryfields.readthedocs.io/en/latest/>`__,
#    GBSApps uses a combination of algorithms available in the `Hafnian
#    <https://hafnian.readthedocs.io/en/latest/>`__ library to carry out sampling from GBS.
#    Nevertheless, simulating GBS is a computationally tough task, and smaller PCs may exhibit a
#    slower sample rate for :func:`~gbsapps.graph.dense_subgraph.dense_subgraph_sampler_gbs` with
#    increasing graph and target subgraph size.
