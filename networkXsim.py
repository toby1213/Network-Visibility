import networkx as nx
import matplotlib.pyplot as plt
import time

# cost of selecting a node
def cost_node(node):
    return 1
    return int(node)

def max_hops_allowed(node):
    return 2


def generate_graph(n, p):
    G = nx.gnp_random_graph(n, p, directed=True)
    # delete isolated nodes
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)
    # find the biggest strongly connected component(SCC)
    strong_components = list(nx.strongly_connected_components(G))
    largest_component = max(strong_components, key=len)
    # the new graph
    G_largest = G.subgraph(largest_component).copy()
    # relable the node IDs
    G_largest = nx.relabel_nodes(G_largest, {old: new for new, old in enumerate(G_largest.nodes())})
    return G_largest

def approximate_greedy(G_largest):
    # all the nodes
    U = set(G_largest.nodes)
    I = set()  # nodes already covered
    sets = []  # every subset of nodes covered each time

    # BFS
    def get_neighbors_within_hops(node, hops):
        """get all neighbors within limited hops"""
        neighbors = set()
        current_level = {node}
        for _ in range(hops):
            next_level = set()
            for n in current_level:
                next_level.update(G_largest.neighbors(n))
            neighbors.update(next_level)
            current_level = next_level
        return neighbors


    # approximate greedy algorithm
    while I != U:
        # the most economic set to cover
        best_set = None
        best_ratio = float('inf')
        nodes_tested = set()
        best_node = None
        
        for node in G_largest.nodes:
            if node not in nodes_tested:
                # nodes_tested.add(node)
                # neighbors = set(G_largest.neighbors(node))
                neighbors = get_neighbors_within_hops(node, max_hops_allowed(node))
                monitored = neighbors | {node}
                new_elements = monitored - I
                if new_elements:
                    ratio = cost_node(node) / len(new_elements)
                    if ratio < best_ratio:
                        best_ratio = ratio
                        best_set = new_elements
                        best_node = node
        
        # update covered nodes
        print(f"choose node {best_node} to cover")
        print(f"{best_set} covered")
        if best_set:
            I.update(best_set)
            sets.append(best_set)

    print(f"chose {len(sets)} subsets to cover all nodes")
    print(f"order of covering: {sets}") 
    return sets

    # # visualize graph
    # pos = nx.spring_layout(G_largest)  # use spring layout
    # nx.draw(G_largest, pos, with_labels=True, node_size=300, node_color="lightblue", arrows=True)
    # plt.show()

# assess the algorithm, n is the number of nodes, p is the probability of edge generation
def assess_algorithm(n, p):
    G = generate_graph(n, p)
    print(f"#nodes: {G.number_of_nodes()}")
    print(f"#edges: {G.number_of_edges()}")

    start_time = time.time()
    
    approx_sets = approximate_greedy(G)
    
    end_time = time.time()
    
    # compute approximation ratio
    # can add baseline here
    optimal_sets = len(approx_sets)  
    # 1 for now, how to get the optimal solution?
    optimal_solution = 1
    approximation_ratio = optimal_sets / optimal_solution

    print(f"approx algo run time: {end_time - start_time:.4f} seconds")
    print(f"approx ratio: {approximation_ratio:.4f}")


if __name__ == "__main__":
    assess_algorithm(1000, 0.01)

