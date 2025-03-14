import numpy as np
from itertools import product
from typing import List
class Polygonalizer():
    def __init__(self):
        pass

    @classmethod
    def polygonalizing_by_trajectory(cls, trajectory, dim = 2):
        """
        Connect multi-valued function points to form polygonal approximations.
        
        Parameters:
        - vectors: List of tuples (x_i, [y_i1, y_i2, ...]) in R^k
        
        Returns:
        - List of line segment lists [[(p_i, p_j)]]
        """
        n = len(trajectory)

        def all_transitions(points_i, points_j):
            points_i = np.array(points_i).reshape((-1, dim))
            points_j = np.array(points_j).reshape((-1, dim))

            len_i = points_i.shape[0]
            len_j = points_j.shape[0]
            result = [[points_i[i], points_j[j]] for j in range(len_j) for i in range(len_i)]
            return result
        
        return np.array([all_transitions(trajectory[i], trajectory[i + 1])
                for i in range(n - 1)]).reshape(-1, 2, dim)