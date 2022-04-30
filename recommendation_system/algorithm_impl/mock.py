from numbers import Number
from typing import List

from recommendation_system.recommendation_algorithm import Algorithm
from recommendation_system.types.recommendation_types import PID, SimulationData


class MockAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    def recommend(self, samples: List[SimulationData], set_point: Number):
        return PID(1.1, 0.5, 1.4)
