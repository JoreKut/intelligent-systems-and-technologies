import networkx as nx
from matplotlib import pyplot as plt

from task_2_vk_graph.models import UserFriends


def get_graph(
        data: list[UserFriends],
        draw_graph=False,
) -> nx.Graph:
    G = nx.Graph()

    for res in data:
        user_id = res.user_id
        friend_ids = res.friend_ids

        G.add_nodes_from(friend_ids + [user_id])
        G.add_edges_from((user_id, friend_id) for friend_id in friend_ids)

    if draw_graph:
        _graw_graph(G)

    return G


def _graw_graph(g: nx.Graph):
    pos = nx.spring_layout(g, k=3)  # k=2 увеличивает расстояние между узлами
    plt.figure(figsize=(10, 10), dpi=500)  # figsize=(10, 10) увеличивает размер, dpi=200 увеличивает разрешение
    nx.draw(
        g,
        pos,
        with_labels=True,
        node_size=20,
        font_size=4,
        font_color='black',
        font_weight='bold'
    )
    plt.show()
