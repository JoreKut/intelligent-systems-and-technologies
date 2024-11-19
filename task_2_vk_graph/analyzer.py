import time
from concurrent.futures import ProcessPoolExecutor

from igraph import Graph as iGraph
from networkx import Graph, betweenness_centrality, eigenvector_centrality, closeness_centrality


def _betweenness_centrality_igraph(graph):
    # Центральность по посредничеству
    print("Analyze betweenness start")
    start_time = time.time()
    igraph, node_map = _convert_networx_to_igraph(graph)

    res_ = igraph.betweenness()
    res = _restore_labels(res_, node_map)

    print(f"Analyze betweenness finish in {time.time() - start_time:2f}s")

    return res


def _betweenness_centrality_networkx(graph):
    # Центральность по посредничеству
    print("Analyze betweenness start")
    start_time = time.time()
    res = betweenness_centrality(graph, normalized=False)
    print(f"Analyze betweenness finish in {time.time() - start_time:2f}s")
    return res


def _eigenvector_centrality(graph):
    # Близость собственного вектора
    print("Analyze eigenvector start")
    start_time = time.time()
    res = eigenvector_centrality(graph, max_iter=10000)
    print(f"Analyze eigenvector finish in {time.time() - start_time:2f}s")
    return res

def _closeness_centrality(graph):
    # Центральность близости
    print("Analyze closeness start")
    start_time = time.time()
    res = closeness_centrality(graph)
    print(f"Analyze closeness finish in {time.time() - start_time:2f}s")
    return res


class GraphAnalyzer:

    def __init__(self, graph: Graph):
        self.graph = graph

    def analyze(self):
        # Запуск функций в отдельных процессах
        with ProcessPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(_betweenness_centrality_igraph, self.graph)
            future2 = executor.submit(_eigenvector_centrality, self.graph)
            future3 = executor.submit(_closeness_centrality, self.graph)

            # Ожидание завершения трёх функций
            betweenness = future1.result()
            eigenvector = future2.result()
            closeness = future3.result()

        return betweenness, eigenvector, closeness


from operator import itemgetter


def show_analyze(graph: Graph) -> (dict[int, float], dict[int, float]):
    print("Analyze graph ", graph)

    result = GraphAnalyzer(graph)
    betweenness_result, eigenvector_result, closeness_result= result.analyze()

    print("Анализ графа:")
    print("-" * 40)

    # Сортировка междуцентральной центральности по убыванию
    sorted_betweenness = dict(sorted(betweenness_result.items(), key=itemgetter(1), reverse=True))
    # Сортировка собственной векторной центральности по убыванию
    sorted_eigenvector = dict(sorted(eigenvector_result.items(), key=itemgetter(1), reverse=True))

    # Сортировка собственной векторной центральности по убыванию
    sorted_closeness = dict(sorted(closeness_result.items(), key=itemgetter(1), reverse=True))

    # Вывод топ-5 узлов для каждой центральности
    print("Центральность по посредничеству:")
    for node, centrality in list(sorted_betweenness.items())[:5]:
        print(f"{node}: {centrality}")

    print("\nЦентральность по собственному вектору:")
    for node, centrality in list(sorted_eigenvector.items())[:5]:
        print(f"{node}: {centrality}")
    
    print("\nЦентральность по близости вектора:")
    for node, centrality in list(sorted_closeness.items())[:5]:
        print(f"{node}: {centrality}")

    print("-" * 40)
    return sorted_betweenness, sorted_eigenvector, sorted_closeness


def _convert_networx_to_igraph(nx_graph: Graph) -> (iGraph, dict[int, int]):  # return graph and Dict[label, idx]
    # Получаем список уникальных узлов
    nodes = list(nx_graph.nodes())
    # Создаем отображение меток узлов в индексы
    node_map = {}
    reverse_node_map = {}
    for idx, node in enumerate(nodes):
        node_map[node] = idx
        reverse_node_map[idx] = node
    # Преобразуем рёбра в индексы
    edges = [(node_map[u], node_map[v]) for u, v in nx_graph.edges()]

    # Создаем граф в igraph
    ig_graph = iGraph()
    ig_graph.add_vertices(len(nodes))
    ig_graph.vs['label'] = nodes  # Сохраняем имена узлов как атрибуты
    ig_graph.add_edges(edges)
    return ig_graph, reverse_node_map


def _restore_labels(vertex_scores_list: list[float], labels_by_idx: dict[int, int]) -> dict[int, float]:
    scores_by_labels = {}
    for n, r in enumerate(vertex_scores_list):
        node_label = labels_by_idx[n]
        scores_by_labels[node_label] = r
    return scores_by_labels
