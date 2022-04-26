from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate, optimize

from recommendation_system.recommendation_algorithm import Algorithm
from recommendation_types import PID, SimulationData

SLOPE_NEAR_ZERO = "Slope approaches zero"


def normalize_data(data):
    min_time = min(data["time"])
    return {
        "output": data["output"],
        "time": list(map(lambda time: time - min_time, data["time"]))
    }


def interpolate_data(xs, ys, slope_thresh=10 ** (-3)):
    plt.plot(xs, ys)
    plt.show()
    func = interpolate.UnivariateSpline(xs, ys)
    derivate_once = func.derivative(n=1)
    derivated_twice = derivate_once.derivative(n=1)
    x_root_of_second_derivative = optimize.root(derivated_twice, x0=np.array([[1.]]))['x'][0]
    point = (x_root_of_second_derivative, func(x_root_of_second_derivative).item())
    slope = derivate_once(x_root_of_second_derivative).item()
    if abs(slope) < slope_thresh:
        return None, None, SLOPE_NEAR_ZERO
    return point, slope, None


def samples_to_data_dict(samples: List[SimulationData]) -> dict:
    time = list(map(lambda sample: sample.timestamp, samples))
    output = list(map(lambda sample: sample.process_value, samples))
    return {
        "time": time,
        "output": output
    }


class ZieglerNichols(Algorithm):

    def __init__(self):
        super().__init__()

    def recommend(self, samples: List[SimulationData], set_point):
        data = samples_to_data_dict(samples)
        normalized_data = normalize_data(data)
        inflection_point, gradient, err_message = interpolate_data(normalized_data["time"], normalized_data["output"])
        return self.calculate_pid(inflection=inflection_point, gradient=gradient, set_point=set_point)

    def calculate_pid(self, inflection, gradient, set_point):
        # inflection: point where 2nd derivative = 0 and closest to origin
        # gradient: the gradient at the point
        # Ziegler Nicols method
        # tangent: y - y1 = m(x - x1)
        # tangent_inversed: (y - y1 + mx1)/m = x
        x, y = inflection
        tangent_inversed = lambda output: (output - y + gradient * x) / gradient
        L = tangent_inversed(0)
        T = tangent_inversed(set_point) - L
        K_p = 1.2 * (T / L)
        K_i = 2 * L
        K_d = 0.5 * L
        return PID(K_p, K_i, K_d)

    # TODO make it safer for data
