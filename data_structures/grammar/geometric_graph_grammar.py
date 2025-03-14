import numpy as np
from typing import List
from numpy.typing import NDArray
from data_structures.geometric_graph import GeometricGraph

class GeometricGraphGrammar:
    def __init__(self):
        self.production_rules : List[GeometricGraphGrammarProdutionRule] = []
    
class GeometricGraphVertexGeometricConnectionProperty:
    def __init__(self, vertex: NDArray, dim, P: NDArray):
        self.vertex: NDArray = vertex
        self.T:NDArray = np.zeros((dim, dim))
        self.P: NDArray = P

class GeometricGraphGrammarProdutionRule:
    def __init__(self, graph: GeometricGraph, lhs_symbol = None, \
                 B: List[GeometricGraphVertexGeometricConnectionProperty] = []):
        self.lhs_symbol = lhs_symbol
        self.B = B
        self.graph = graph
