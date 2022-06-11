import unittest

import control as control
import control.matlab as matlab
import numpy as np

from recommendation_system.algorithm_impl.ziegler_nichols import ZieglerNichols
from recommendation_system.types.recommendation_types import SimulationData, PID


def simulation_data_from_values(T, p, i, d, Y, U, R):
    params = list(zip(T, Y, U, R))
    ret = []
    for time, process_value, pid_value, set_point in params:
        ret = ret + [SimulationData(time, process_value, set_point, pid_value, PID(p, i, d))]
    return ret


class TestZieglerNichols(unittest.TestCase):
    def test_algo(self):
        expected_p = -64
        expected_i = 224
        expected_d = 56
        legal_deviation = 0.5

        setpoint = 100
        duration = 25
        sampling_delta = .01
        T = np.arange (0, duration, sampling_delta)
        samples_amount = T.shape[0]
        R = np.ones(samples_amount)
        plant = matlab.tf([1,4,5], [4,1, 3])
        T, Y = control.forced_response(plant, T, R)
        U = Y
        sim_data = simulation_data_from_values(T, 0, 0, 0, Y, U, R)
        recommendation = ZieglerNichols().recommend(sim_data, setpoint)
        p, i ,d = recommendation.p, recommendation.i, recommendation.d
        assert abs(expected_p - p) < legal_deviation
        assert abs(expected_i - i) < legal_deviation
        assert abs(expected_d - d) < legal_deviation