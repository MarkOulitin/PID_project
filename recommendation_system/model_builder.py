from typing import List

from control import *
from numpy import matmul, around
from numpy.linalg import inv

from recommendation_system.types.recommendation_types import SimulationData


class ModelBuilder:
    def __init__(self, simulation_data: List[SimulationData]):
        self.simulation_data = simulation_data

    def get_IO_of_plant(self):
        # U input, Y output
        u = list(map(lambda sim_data: sim_data.pid_value, self.simulation_data))
        y = list(map(lambda sim_data: sim_data.process_value, self.simulation_data))
        return y, u

    def fit(self):
        Y, U = self.get_IO_of_plant()
        for i in range(10, 500, 10):
            h = None
            for j in range(len(Y) - 10 - 1, 0, -1):
                try:
                    y = Y[j:j + i]
                    u = U[j:j + i]
                    h = markov(y, u)[0]
                    break
                except:
                    pass
            if h is not None:
                break

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
