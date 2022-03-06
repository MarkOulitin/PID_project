import numpy as np
from control.matlab import *


class ModelBuilder:
    def __init__(self):
        pass

    def fit(self):
        model = tf(
            np.array([1]),  # numerator
            np.array([1, 1])  # denumerator
        )
        return model
