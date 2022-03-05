from numbers import Number
from typing import List


class PID:
    def __init__(self,
                 p: Number,
                 i: Number,
                 d: Number):
        self.p = p
        self.i = i
        self.d = d


class SimulationData:  # each represents an entry in samples db
    def __init__(self,
                 timestamp: Number,
                 pid: PID,
                 process_value: Number,
                 pid_value: Number,
                 set_point: Number):
        self.timestamp = timestamp
        self.pid = pid
        self.process_value = process_value
        self.pid_value = pid_value
        self.set_point = set_point


class RecommendationRequest:
    def __init__(self,
                 set_point: Number,  # needed for simulation - for tom - fetch from lazy sampler
                 pid: PID,  # needed for model fitting and simulation - tom for fetch from lazy sampler
                 convergence_time: Number,  # needed for simulation - for tom - seconds + minutes from request
                 simulation_data: List[SimulationData],  # needed for model fitting - for tom - from db
                 current_sensor_value: Number
                 ):
        self.set_point = set_point
        self.pid = pid
        self.convergence_time = convergence_time
        self.simulation_data = simulation_data
        self.current_sensor_value = current_sensor_value

class PidDataPoints: 
    def __init__(self,
                 time,
                 amplitude
                 ) -> None:
        self.time = time
        self.amplitude = amplitude

class RecommendationResult:
    def __init__(self,
                 old_pid,
                 old_pid_data_points,
                 recommended_pid,
                 recommended_pid_data_points,
                 ) -> None:
        self.old_pid = old_pid
        self.old_pid_data_points = old_pid_data_points
        self.recommended_pid = recommended_pid
        self.recommended_pid_data_points = recommended_pid_data_points

class PLC:
    def __init__(self, name):
        self.name = name
