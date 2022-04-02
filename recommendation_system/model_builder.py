import numpy as np
from control.matlab import *
from control import *
import numpy as np
from numpy.linalg import matrix_rank, inv
from numpy import matmul, around
from typing import List

from recommendation_types import SimulationData


class ModelBuilder:
    def __init__(self, simulation_data: List[SimulationData]):
        self.__data_points = simulation_data

    def get_IO_of_plant():
        # TODO implement
        return [], []

    def fit(self):
        Y, U = self.get_IO_of_plant()
        h = markov(Y, U)[0]

        def H(nr, nc, dr=0, dc=0):
            return np.array([[round(h[dc + dr * dc + j + 1]) for j in range(i, i + nc)] for i in range(nr)])

        M = H(2, 2)
        MA = H(2, 2, 0, 1)
        MC = H(1, 2)
        MB = H(2, 1)
        
        A = around(matmul(MA, inv(M)))
        b = around(MB)
        c = around(matmul(MC, inv(M)))
        d = round(h[0])

        model = ss2tf(A, b, c, d)
        return model
