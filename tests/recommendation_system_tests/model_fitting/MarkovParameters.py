import control as control
import scipy.integrate as integrate
import scipy.fft as fft
import pandas as pd
import control.matlab as matlab
import numpy as np
from numpy.linalg import matrix_rank, inv
from numpy import matmul, around
import matplotlib.pyplot as plt

from recommendation_system.model_builder import ModelBuilder

def main():
    duration = 25
    sampling_delta = 1
    T = np.arange (0, duration, sampling_delta)
    samples_amount = T.shape[0]
    R = np.ones(samples_amount)
    # plant = control.sample_system(matlab.tf([1], [1, 1]),.1)
    plant = control.sample_system(matlab.tf([1,4,5], [4,1, 3]),.1)

    p = 1.1
    i = 1.6
    d = 1
    pid_model = matlab.tf(
                # d  p   i 
                [p+i+d, i-p-2*d, d],  # numerator
                [1, -1, 0],  # denumerator
                .1
            )
    # encapsulate pid tf and the plant to one tf
    open_loop = matlab.series(pid_model, plant)
    # encapsulate open loop wit feedback response signal
    closed_loop = matlab.feedback(open_loop, [1])
    T, Y = control.forced_response(closed_loop, T, R)
    E = R - Y
    p = 1.6
    i = 1
    d = 0.5
    def pid_func(T, E):
        s = fft.fft(E)
        y_s = p + i / s + d * s
        return fft.ifft(y_s)
    U = pid_func(T,E).real
    model_builder = ModelBuilder()
    infered_model = model_builder.fit()
    plant_numerator = plant.num[0][0] 
    plant_denumerator = plant.den[0][0]
    infered_numerator = infered_model.num[0][0] 
    infered_denumerator = infered_model.den[0][0]
    assert len(plant_numerator) == len(infered_numerator)
    assert len(plant_denumerator) == len(infered_denumerator)
    for num_i, infered_num_i in zip(plant_numerator, infered_numerator):
        assert num_i == infered_num_i
    for den_i, infered_den_i in zip(plant_denumerator, infered_denumerator):
        assert den_i == infered_den_i

if __name__ == "__main__":
    main()
