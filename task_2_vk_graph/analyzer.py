import time
from concurrent.futures import ThreadPoolExecutor
from networkx import Graph, betweenness_centrality, eigenvector_centrality
from operator import itemgetter

def _betweenness_centrality(graph):
    # Центральность по посредничеству
    print("Analyze betweenness start")
    start_time = time.time()
    res = betweenness_centrality(graph)
    print(f"Analyze betweenness finish in {time.time() - start_time:2f}s")
    return res

def _eigenvector_centrality(graph):
    # Близость собственного вектора
    print("Analyze eigenvector start")
    start_time = time.time()
    res =  eigenvector_centrality(graph)
    print(f"Analyze eigenvector finish in {time.time() - start_time:2f}s")
    return res

class GraphAnalyzer:

    def __init__(self, graph: Graph):
        self.graph = graph

    def analyze(self):
        # Запуск функций в отдельных потоках
        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(_betweenness_centrality, self.graph)
            future2 = executor.submit(_eigenvector_centrality, self.graph)

            # Ожидание завершения обеих функций
            betweenness = future1.result()
            eigenvector = future2.result()

        return betweenness, eigenvector

from operator import itemgetter

def show_analyze(graph: Graph) -> (list[int], list[int]):
    print("Analyze graph ", graph)

    result = GraphAnalyzer(graph)
    betweenness_result, eigenvector_result = result.analyze()
    
    print("Анализ графа:")
    print("-" * 40)
    
    # Сортировка междуцентральной центральности по убыванию
    sorted_betweenness = dict(sorted(betweenness_result.items(), key=itemgetter(1), reverse=True))
    # Сортировка собственной векторной центральности по убыванию
    sorted_eigenvector = dict(sorted(eigenvector_result.items(), key=itemgetter(1), reverse=True))
    
    # Вывод топ-5 узлов для каждой центральности
    print("Центральность по посредничеству:")
    for node, centrality in list(sorted_betweenness.items())[:5]:
        print(f"{node}: {centrality}")

    print("\nБлизость собственного вектора:")
    for node, centrality in list(sorted_eigenvector.items())[:5]:
        print(f"{node}: {centrality}")
    
    print("-" * 40)
    return list(sorted_betweenness.keys()), list(sorted_eigenvector.keys())


