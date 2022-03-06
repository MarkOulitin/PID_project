from numbers import Number
from typing import List

from recommendation_system.recommendation_algorithm import Algorithm
from recommendation_types import PID
from sample import Sample


class MockAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    def recommend(self, samples: List[Sample], set_point: Number):
        return PID(1.1, 0.5, 1.4)
