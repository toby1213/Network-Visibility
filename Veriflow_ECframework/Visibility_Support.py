import networkx as nx
import matplotlib.pyplot as plt
import time
from .VeriFlow.Network import Network
from .VeriFlow.Interval import Interval

# get networkx subgraph according to the EC user selected
def get_subgraph(ec, network):
    # 创建一个新的有向图
    G = nx.DiGraph()

    # 解析EC字符串为Interval对象
    ec_parts = ec.strip('[').strip(']').split(',')
    ec_interval = Interval(ec_parts[0], ec_parts[1])

    # 添加所有交换机作为节点
    for switch_id, switch in network.switches.items():
        G.add_node(switch_id)

    # 遍历所有交换机，添加与EC相关的边
    for switch_id, switch in network.switches.items():
        rule = switch.getAssociatedRule(ec_interval.getLeft())
        if rule:
            next_hop_id = rule.getNextHopId()
            if next_hop_id in network.switches:
                # 如果下一跳是交换机，添加一条有向边
                G.add_edge(switch_id, next_hop_id)
            elif next_hop_id in network.hosts:
                # 如果下一跳是主机，添加主机节点和边
                G.add_node(next_hop_id, type='host')
                G.add_edge(switch_id, next_hop_id)

    # 移除孤立的节点（没有边连接的交换机）
    G.remove_nodes_from(list(nx.isolates(G)))

    return G

# 辅助函数：将二进制字符串转换为IP地址
def binary_to_ip(binary_str):
    # 确保二进制字符串长度为32位
    binary_str = binary_str.zfill(32)
    # 每8位转换为一个十进制数
    octets = [str(int(binary_str[i:i+8], 2)) for i in range(0, 32, 8)]
    return ".".join(octets)

# 修改主函数以使用新的EC格式
def main():
    import os
    print("Current working directory:", os.getcwd())
    network = Network()
    network.parseNetworkFromFile("./Veriflow_ECframework/Topo/Complex-Topo.txt")
    generatedECs = network.getECsFromTrie()
    network.checkWellformedness()
    network.log(generatedECs)
    
    # 假设这些是从网络中获取的ECs
    ecs = [
        "[00,01)",
        "[100,1001)",
        "[0110,0111)",
        "[1001,1010)",
        "[110,111)",
        "[010,011)",
        "[111,End)",
        "[101,110)",
        "[0111,100)"
    ]

    # 选择一个EC（这里假设我们选择第一个EC）
    selected_ec = ecs[0]

    # 获取子图
    subgraph = get_subgraph(selected_ec, network)

    # 打印节点和边
    print("Nodes:", subgraph.nodes())
    print("Edges:", subgraph.edges())

    # 现在你可以使用networkx的功能来分析或可视化这个子图
    # 例如，打印节点的IP地址
    for node in subgraph.nodes():
        print(f"Node IP {node}")

if __name__ == "__main__":
    main()
    