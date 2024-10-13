from networkx import Graph, betweenness_centrality, eigenvector_centrality

class GraphAnalyzer:
    def __init__(self, graph: Graph):
        self.graph = graph

    def analyze(self):
        # Центральность по посредничеству
        betweenness = betweenness_centrality(self.graph)
        
        # Близость собственного вектора
        eigenvector = eigenvector_centrality(self.graph)
        
        return betweenness, eigenvector

def show_analyze(graph: Graph):
    result = GraphAnalyzer(graph)
    betweenness_result, eigenvector_result= result.analyze()
    
    print("Анализ графа:")
    print(f"Центральность по посредничеству: {betweenness_result}")
    print(f"Близость собственного вектора: {eigenvector_result}")
