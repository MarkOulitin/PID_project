import control as control
import scipy.integrate as integrate
import scipy.fft as fft
import pandas as pd
import control.matlab as matlab
import numpy as np
from numpy.linalg import matrix_rank, inv
from numpy import matmul, around
import matplotlib.pyplot as plt

def main():
    duration = 25
    sampling_delta = .01
    T = np.arange (0, duration, sampling_delta)
    samples_amount = T.shape[0]
    R = np.ones(samples_amount)
    plant = matlab.tf([1,4,5], [4,1, 3])
    T, Y = control.forced_response(plant, T, R)
    

if __name__ == "__main__":
    main()