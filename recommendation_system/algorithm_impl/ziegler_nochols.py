

from recommendation_system.recommendation_algorithm import Algorithm
from recommendation_types import PID


class ZieglerNichols(Algorithm):

    def __init__(self):
        super().__init__()
    
    def recomend(self):
        return PID(1.1, 0.5, 1.4)