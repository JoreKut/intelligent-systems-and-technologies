import networkx as nx

from task_2_vk_graph.models import GetUserFriendsResponse


def get_graph(data: list[GetUserFriendsResponse]) -> nx.Graph:
    ...
