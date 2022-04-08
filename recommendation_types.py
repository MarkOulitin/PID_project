from io import StringIO
from numbers import Number
from typing import List, Dict, Any

import numpy
import pandas
from pandas import DataFrame
from datetime import datetime

from werkzeug.datastructures import FileStorage


class PID:
    def __init__(self,
                 p: Number,
                 i: Number,
                 d: Number):
        self.p = p
        self.i = i
        self.d = d


class SimulationData:  # each represents an entry in samples db
    def __init__(self, timestamp: Number, process_value: Number, set_point: Number, out_value: Number, pid: PID = None):
        self.timestamp = timestamp
        self.pid = pid
        self.process_value = process_value
        self.pid_value = out_value
        self.set_point = set_point


def normalize_down(simulations_data: List[SimulationData]) -> List[SimulationData]:
    ret: List[SimulationData] = []
    pv, st, out = float("nan"), float("nan"), float("nan")
    for simulations_data in simulations_data:
        if simulations_data.process_value == 0:
            pass
        pv, st, out = \
            pv if simulations_data.process_value != simulations_data.process_value or simulations_data.process_value is None else simulations_data.process_value, \
            st if simulations_data.set_point != simulations_data.set_point or simulations_data.set_point is None else simulations_data.set_point, \
            out if simulations_data.pid_value != simulations_data.pid_value or simulations_data.pid_value is None else simulations_data.pid_value
        ret.append(SimulationData(simulations_data.timestamp, pv, st, out))
    return ret


def simulation_data_from_file(file: FileStorage) -> List[SimulationData]:
    f = pandas.read_csv(file.stream, skiprows=1, encoding="utf-8")
    ret: List[SimulationData] = []
    for row_tuple in f.iterrows():
        row = row_tuple[1]
        timestamp = int(round(float(datetime.strptime("{} {} {}000".format(row.get(1), row.get(2), row.get(3)),
                                                      "%d/%m/%Y %H:%M:%S %f").timestamp() * 1000)))
        set_point = float(row.get(4))
        process_value = float(row.get(5))
        out_value = float(row.get(6))
        ret.append(SimulationData(timestamp, process_value, set_point, out_value))
    return normalize_down(ret)


class RecommendationRequest:
    # todo after loading the simmulation data, fill missing values from the past value. if it doesnt exist, delete row.
    #  it too many rows deleted, throw exception
    def __init__(self,
                 set_point_goal: Number,
                 pid: PID,
                 convergence_time: Number,
                 simulation_data: List[SimulationData]):
        self.set_point = set_point_goal
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
                 old_pid: PID,
                 old_pid_data_points: PidDataPoints,
                 recommended_pid: PID,
                 recommended_pid_data_points: PidDataPoints,
                 ) -> None:
        self.old_pid = old_pid
        self.old_pid_data_points = old_pid_data_points
        self.recommended_pid = recommended_pid
        self.recommended_pid_data_points = recommended_pid_data_points


class PLC:
    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    with open('/Users/tomsandalon/Downloads/TEST2.csv', 'rb') as fp:
        a = simulation_data_from_file(FileStorage(fp))
        print(a)
