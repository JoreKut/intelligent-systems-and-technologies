from typing import Iterable

import networkx as nx
from pyvis.network import Network

from task_2_vk_graph.file_service import BASE_STORAGE_DIRECTORY
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
        main_nodes: list[int],
        min_edges: int = 1,
):  # main_nodes – ноды, которые нужно оставить в графе и их связи
    graph = g.copy()

    print(f"Draw graph, with main nodes ({len(main_nodes)}) {main_nodes} ")
    print(f"Graph has {len(graph.nodes)} nodes")

    print("Prepare graph...")
    left_nodes = set(main_nodes)
    for node in main_nodes:
        neighbors = set(graph.neighbors(node))
        left_nodes.update(neighbors)
    remove_nodes = set(graph.nodes) - left_nodes

    print(f"Need to remove {len(remove_nodes)} nodes")
    graph.remove_nodes_from(remove_nodes)
    print(f"Graph has {len(graph.nodes)} nodes")

    print("Clear dangling nodes")
    _clear_dangling_edges(graph, min_edges=min_edges)
    print(f"Graph has {len(graph.nodes)} nodes")

    net = _transform_ntworkx_to_pyvis(graph, main_nodes)

    net.barnes_hut()  # нормальная физика
    net.show(f"{BASE_STORAGE_DIRECTORY}/graph.html", notebook=False)


def _clear_dangling_edges(graph: nx.Graph, min_edges=1) -> int:
    nodes_to_remove = [
        n for n, degree in dict(graph.degree()).items()
        if int(degree) < min_edges
    ]
    if not nodes_to_remove:
        return 0
    graph.remove_nodes_from(nodes_to_remove)
    return len(nodes_to_remove)


def _transform_ntworkx_to_pyvis(
        graph: nx.Graph,
        main_nodes: list[int],
) -> Network:
    net = Network()

    for n, node in enumerate(graph.nodes()):
        opts = {"label": str(node)}
        if node in main_nodes:
            opts.update({"color": "#eb4c34"})
        net.add_node(node, **opts)

    for edge in graph.edges():
        try:
            net.add_edge(edge[0], edge[1])
        except:
            pass

    return net
