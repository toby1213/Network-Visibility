import networkx as nx
import matplotlib.pyplot as plt
import time
from Veriflow_ECframework.VeriFlow.Network import Network
import Veriflow_ECframework.Visibility_Support as Visibility_Support

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
    nodes_tested = set()    # nodes that have been tested and examined doesn't need to be tested again
    while I != U:
        # the most economic set to cover
        best_set = None
        best_ratio = float('inf')
        
        best_node = None
        
        for node in G_largest.nodes:
            if node not in nodes_tested:
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
        nodes_tested.add(best_node)
        
        # update covered nodes
        print(f"choose node {best_node} to cover")
        print(f"{best_set} covered")
        if best_set:
            I.update(best_set)
            sets.append(best_set)

    print(f"chose {len(sets)} subsets to cover all nodes")
    print(f"order of covering: {sets}") 

    return sets

    # visualize graph
    pos = nx.spring_layout(G_largest)  # use spring layout
    nx.draw(G_largest, pos, with_labels=True, node_size=300, node_color="lightblue", arrows=True)
    plt.show()

# assess the algorithm, n is the number of nodes, p is the probability of edge generation
# assess the algorithm on a random graph
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


def find_ec_for_ip(ip_address, ecs):
    """
    判断IP地址属于哪个等价类
    
    参数:
    ip_address: 字符串，标准IP地址格式，如 "192.1.1.1"
    ecs: 等价类列表，每个等价类是包含二进制字符串的区间
    
    返回:
    匹配的等价类的字符串表示，如"[00,01)"，如果没有找到则返回None
    """
    def ip_to_binary(ip):
        # 分割IP地址
        parts = ip.split('.')
        if len(parts) != 4:
            return None
        
        # 检查每个部分是否为有效数字
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return None
        
        # 转换为二进制字符串
        binary = ''
        for part in parts:
            binary += format(int(part), '08b')
        return binary

    # 将IP转换为二进制
    ip_binary = ip_to_binary(ip_address)
    if not ip_binary:
        return None
    
    # 遍历所有等价类寻找匹配
    for ec in ecs:
        left = ec.getLeft()
        right = ec.getRight()
        
        # 处理End情况
        if right == "End":
            right = "1" * len(left)
        
        # 确保二进制串长度匹配
        ip_binary_trimmed = ip_binary[:len(left)]
        
        # 比较是否在区间内
        if left <= ip_binary_trimmed <= right:
            # 返回半开区间格式的字符串
            return f"[{left},{right})"
            
    return None


# assess algorithm on Veriflow_ECframework (supports ECs)
def assess_approx_EC():
    network = Network()
    network.parseNetworkFromFile("./Veriflow_ECframework/Topo/Complex-Topo.txt")
    generatedECs = network.getECsFromTrie()
    network.checkWellformedness()
    network.log(generatedECs)
    # print switch list
    print("Switches: ");
    for switch in network.switches:
        print(switch);
	# print EC list
    print("ECs: ");
    for ec in generatedECs:
        print(ec.toString());
    
    # 选择一个EC（这里假设我们选择第一个EC）
    # selected_ec = input("Enter the EC you want to choose: ")
    ip_address = input("Enter the IP address you want to classify: ")
    selected_ec = find_ec_for_ip(ip_address, generatedECs)
    print(f"selected EC: {selected_ec}")

    # 获取子图
    subgraph = Visibility_Support.get_subgraph(selected_ec, network)

    start_time = time.time()
    
    approx_sets = approximate_greedy(subgraph)
    
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
    # assess_algorithm(1000, 0.01)
    assess_approx_EC()

