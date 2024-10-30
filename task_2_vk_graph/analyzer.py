from networkx import Graph, betweenness_centrality, eigenvector_centrality
from operator import itemgetter

class GraphAnalyzer:

    def __init__(self, graph: Graph):
        self.graph = graph

    def analyze(self):
        # Центральность по посредничеству
        betweenness = betweenness_centrality(self.graph)
        
        # Близость собственного вектора
        eigenvector = eigenvector_centrality(self.graph)
        
        return betweenness, eigenvector

from operator import itemgetter

def show_analyze(graph: Graph):
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


