import networkx as nx
from matplotlib import pyplot as plt

from task_2_vk_graph.models import GetUserFriendsResponse


def get_graph(
        data: list[GetUserFriendsResponse],
        draw_graph=False,
) -> nx.Graph:
    G = nx.Graph()

    for res in data:
        user_id = res.user_id
        friend_ids = res.items

        G.add_nodes_from(friend_ids + [user_id])
        G.add_edges_from((user_id, friend_id) for friend_id in friend_ids)

    if draw_graph:
        _graw_graph(G)

    return G


def _graw_graph(G: nx.Graph):
    pos = nx.spring_layout(G, k=3)  # k=2 увеличивает расстояние между узлами
    plt.figure(figsize=(10, 10), dpi=500)  # figsize=(10, 10) увеличивает размер, dpi=200 увеличивает разрешение
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=20,
        font_size=4,
        font_color='black',
        font_weight='bold'
    )
    plt.show()
