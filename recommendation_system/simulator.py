from control.matlab import * 
import numpy as np
class Simulator:
    def __init__(self, set_point, pid, model, initial_signal):
        self.__set_point = set_point
        self.__pid = pid
        self.__model = model
        self.__initial_signal = initial_signal

    def simulate(self, t_limit= 10, t_step= 0.01):
        # build pid tf
        pid_model = tf(
            np.array([self.__pid.d, self.__pid.p, self.__pid.i]), # numerator
            np.array([1, 0]) # denumerator
        )
        # encapsulate pid tf and the plant to one tf
        open_loop = series(pid_model, self.__model)
        # encapsulate open loop wit feedback response signal
        closed_loop = feedback(open_loop, [1])
        
        # to samples of system behavior
        time_samples = self.makeTimeSamples(t_limit=t_limit, t_step= t_step)
        u_ref = self.array_map(self.__set_point, np.ones(time_samples.shape))
        # TODO add initial signal as u_input to closed_loop tf. consult with gera about if it's valid. 
        # u_input = self.initial_signal * np.ones(time_samples.shape)
        u_input = np.zeros(time_samples.shape)
        out = lsim(closed_loop, u_ref - u_input, time_samples)
        return out[1], out[0]
    
    def array_map(self, f, array):
        return np.array(list(map(f, array)))
    
    def makeTimeSamples(self, t_limit = 8, t_step = 0.01, t0 = 0):
        samples_amount = int ( t_limit / t_step ) + 1
        ts = np.linspace( t0 , t_limit , samples_amount )
        return ts
    