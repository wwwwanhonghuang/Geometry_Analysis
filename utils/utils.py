from data_structures.geometric_graph import GeometricGraph
from numpy.typing import NDArray
import numpy as np

def geometry_graph_from_segments(segments: NDArray):
    # segments shape = (n, 2, dim). n is the count of vertexes, 2 is represent two points: 
    # start point and end point, dim is the dimension of a point.
    unique_vertexes = set()

    n = segments.shape[0]
    dim = segments.shape[2]

    for i in range(n):
        start_point = tuple(segments[i, 0, :])
        end_point = tuple(segments[i, 1, :])
        unique_vertexes.add(start_point)
        unique_vertexes.add(end_point)
    
    unique_vertexes = list(unique_vertexes)
    vertexes_map = { vertex: index
        for index, vertex in enumerate(unique_vertexes)        
    }

    E = []
    for i in range(n):
        start_point = tuple(segments[i, 0, :])
        end_point = tuple(segments[i, 1, :])
        E.append([vertexes_map[start_point], vertexes_map[end_point]])
        
    V = np.array(unique_vertexes).reshape((-1, dim))

    graph = GeometricGraph(V, E, dim=dim)
    return graph


