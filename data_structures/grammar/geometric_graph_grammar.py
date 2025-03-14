import numpy as np
from typing import List
from numpy.typing import NDArray
from data_structures.geometric_graph import GeometricGraph

class GeometricGraphGrammar:
    def __init__(self, dim = 2):
        self.production_rules : List[GeometricGraphGrammarProdutionRule] = []
        self.dim = dim
        self.symbol_graph_mapping = {

        }
        self.graph_symbol_mapping = {

        }
    def _allocate_new_symbol(self):
        """Generate a new unique symbol for a graph."""
        if not hasattr(self, '_symbol_counter'):
            self._symbol_counter = 0
        self._symbol_counter += 1
        return f'S{self._symbol_counter}'  # Example: S1, S2, S3, ...


    def _new_nonterminate_signal_node_graph(self):
        return GeometricGraph(np.zeros(self.dim), [], dim=self.dim)
    
    def _find_graph(self, graph):
        """Check if a graph already exists in the mapping."""
        for g in self.graph_symbol_mapping:
            if self._are_graphs_equal(g, graph):
                return g
        return None    
    
    def _are_graphs_equal(self, graph1: GeometricGraph, graph2: GeometricGraph):
        """Helper method to check if two graphs are equal."""
        return (np.array_equal(graph1.V, graph2.V) and (graph1.E == graph2.E))
    
    def _remember_graph(self, graph: GeometricGraph, is_terminal):
        remembered_graph = self._find_graph(graph)
        if(remembered_graph):
            return self.graph_symbol_mapping[remembered_graph]
        
        symbol = self._allocate_new_symbol()
        self.symbol_graph_mapping[symbol] = (graph, is_terminal)
        self.graph_symbol_mapping[graph] = symbol
        return symbol

    def add_grammar(self, graph):
        rhs_symbol = self._remember_graph(graph)
        lhs_node = self._new_nonterminate_signal_node_graph()
        rule: GeometricGraphGrammarProdutionRule = GeometricGraphGrammarProdutionRule(
            rhs_symbol, lhs_node)
        self.production_rules.append(rule)
    
class GeometricGraphVertexGeometricConnectionProperty:
    def __init__(self, vertex: NDArray, dim, P: NDArray):
        self.vertex: NDArray = vertex
        self.T:NDArray = np.zeros((dim, dim))
        self.P: NDArray = P

class GeometricGraphGrammarProdutionRule:
    def __init__(self, graph_id: any, lhs_symbol = None, \
                 B: List[GeometricGraphVertexGeometricConnectionProperty] = []):
        self.lhs_symbol = lhs_symbol
        self.B = B
        self.graph_id = graph_id

