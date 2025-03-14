from typing import List
from numpy.typing import NDArray
import numpy as np

class GeometricGraph:
    def __init__(self, V: NDArray, E: List[List[int]] = [], dim = 2):
        self.V : NDArray = V
        self.E : List = E
        self.dim = dim
        assert V.shape[1] == dim, f"V should has the shape (n_vertexes, vertex_dim). dimension 1 == {V.shape[1]} != {dim}" 
    
    @property
    def n_vertexes(self):
        return len(self.V)
    
    def __str__(self):
        return f"(size: {self.n_vertexes}, V = {self.V}, E = {self.E})"

    def __repr__(self):
        return self.__str__()
    
    def copy(self):
        graph = GeometricGraph(np.array(self.V), [list(edge) for edge in self.E], dim=self.dim)
        return graph
    
    def __hash__(self):
        """Hash based on vertices and edges."""
        return hash(tuple(map(tuple, self.V), tuple(self.E)))

    def __eq__(self, other):
        """Equality based on vertices and edges."""
        return (np.array_equal(self.V, other.V) and (self.E == other.E))