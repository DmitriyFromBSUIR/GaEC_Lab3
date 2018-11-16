
#
import math
#
import matplotlib.pyplot as plt
import networkx as nx


class Matrix:
    pass


if __name__ == "__main__":
    G = nx.Graph()

    G.add_node("a", pos=(1, 1))
    G.add_node("b", pos=(2, 2))
    G.add_node("c", pos=(1, 2))
    G.add_node("d", pos=(2, 1))

    '''
    G.add_edge('a', 'b', weight=0.6)
    G.add_edge('a', 'c', weight=0.2)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)
    
    '''

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

    #pos = nx.spring_layout(G)  # positions for all nodes
    pos = nx.get_node_attributes(G, 'pos')

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    #nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    #nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')

    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=6)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.axis('off')
    plt.show()

    # Create a test graph
    #m = 2  # Number of initial links
    n = 6  # Number of nodes
    ncols = 3  # Number of columns in a 10x10 grid of positions
    #G = nx.barabasi_albert_graph(n, m, j)

    # pos = {i: (i // ncols, (n - i - 1) % ncols) for i in G.nodes()}

    # Compute the node-to-node distances
    lengths = {}
    for edge in G.edges():
        startnode = edge[0]
        endnode = edge[1]
        lengths[edge] = round(math.sqrt(((pos[endnode][1] - pos[startnode][1]) ** 2) +
                                        ((pos[endnode][0] - pos[startnode][0]) ** 2)), 2)

    print(lengths)