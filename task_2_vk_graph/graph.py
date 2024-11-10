from typing import Iterable

import networkx as nx
from matplotlib import pyplot as plt

from task_2_vk_graph.models import UserData


def get_graph(
        source: Iterable[UserData],
) -> nx.Graph:
    G = nx.Graph()

    for user_data in source:
        user_id = user_data["user_id"]
        print("\t| [get_graph] process user", user_id)

        friends_ids = user_data["friend_ids"]

        G.add_nodes_from(friends_ids + [user_id])
        G.add_edges_from((user_id, friend_id) for friend_id in friends_ids)

    return G


def draw_graph(
        g: nx.Graph,
        betweenness_result: list[int],
        eigenvector_result: list[int],
):  # left_main_nodes – ноды, которые нужно оставить в графе и их связи
    left_main_nodes = eigenvector_result[:10]

    print("Draw graph...")
    print("Get graph with ", g)
    print(f"Need to left next nodes ({len(left_main_nodes)}) → ", left_main_nodes)

    print("Prepare graph")

    graph = g.copy()

    all_nodes = set(graph.nodes)

    left_nodes = set()
    for node in left_main_nodes:
        neighbors = set(graph.neighbors(node))
        left_nodes.update(neighbors)

    remove_nodes = all_nodes - left_nodes
    print(f"Need to remove next nodes ({len(remove_nodes)}) → ", remove_nodes)
    graph.remove_nodes_from(remove_nodes)

    print(f"Left graph with {len(graph.nodes)} nodes → {graph.nodes}")

    # min_edges_connected = 17
    # n = 0
    # while 1:
    #     nodes_to_remove = [node for node, degree in dict(graph.degree()).items() if degree < min_edges_connected]
    #     if not nodes_to_remove:
    #         break
    #     graph.remove_nodes_from(nodes_to_remove)
    #     n += 1
    #
    # left_nodes = list(dict(graph.degree()).keys())
    # print("left nodes1 ", left_nodes)
    # left_nodes = random.sample(left_nodes, len(left_nodes) - 6)
    # print("left nodes2 ", left_nodes)
    #
    # graph.remove_nodes_from(left_nodes)
    #
    #
    # print(f"clear graph in {n} epochs and left graph with {len(graph.nodes)} nodes")
    #
    #
    # options1 = {
    #     'node_color': 'yellow',
    #     'node_size': 8500,
    #     'width': 1,
    #     'arrowstyle': '-|>',
    #     'arrowsize': 18,
    #     "with_labels": True,
    #     "arrows": True,
    # }
    options2 = {
        "with_labels": True,
        "node_size": 20,
        "font_size": 4,
        "font_color": 'black',
        "font_weight": 'bold'
    }

    pos = nx.spring_layout(graph, k=1000)  # k=2 увеличивает расстояние между узлами
    # pos = nx.spring_layout(g, k=3)  # k=2 увеличивает расстояние между узлами
    plt.figure(figsize=(10, 10), dpi=500)  # figsize=(10, 10) увеличивает размер, dpi=200 увеличивает разрешение
    nx.draw(
        graph,
        pos,
        **options2
    )
    plt.show()
