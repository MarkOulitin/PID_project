import json
from datetime import datetime
from numbers import Number
from typing import List

import pandas
from werkzeug.datastructures import FileStorage


class PID:
    def __init__(self,
                 p,
                 i: Number,
                 d: Number):
        self.p = p
        self.i = i
        self.d = d

    def __eq__(self, other):
        return self.p == other.p and self.i == other.i and self.d == other.d


class SimulationData:  # each represents an entry in samples db
    def __init__(self, timestamp: Number, process_value: Number, set_point: Number, out_value: Number, pid: PID = None):
        self.timestamp = timestamp
        self.pid = pid
        self.process_value = process_value
        self.pid_value = out_value
        self.set_point = set_point

    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.process_value == other.process_value and \
               self.set_point == other.set_point and self.pid_value == other.pid_value and self.pid == other.pid

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def simulation_data_from_dict(d):
    return SimulationData(d["timestamp"], d["process_value"], d["set_point"], d["pid_value"], d.get("PID"))


def normalize_down(simulations_data: List[SimulationData]) -> List[SimulationData]:
    def check_process_value(simulation_data: SimulationData) -> bool:
        return simulation_data.process_value != simulation_data.process_value or simulation_data.process_value is None

    def check_set_point(simulation_data: SimulationData) -> bool:
        return simulation_data.set_point != simulation_data.set_point or simulation_data.set_point is None

    def check_pid_value(simulation_data: SimulationData) -> bool:
        return simulation_data.pid_value != simulation_data.pid_value or simulation_data.pid_value is None

    ret: List[SimulationData] = []
    pv, st, out = float("nan"), float("nan"), float("nan")
    for simulations_data in simulations_data:  # todo remove bad rows
        pv, st, out = \
            pv if check_process_value(simulations_data) else simulations_data.process_value, \
            st if check_set_point(simulations_data) else simulations_data.set_point, \
            out if check_pid_value(simulations_data) else simulations_data.pid_value
        ret.append(SimulationData(simulations_data.timestamp, pv, st, out))
    result = list(filter(lambda row: not (check_process_value(row) or check_set_point(row) or check_pid_value(row)), ret))
    # if float(len(result)) / float(len(ret)) < REQUEST_FILTER_THRESHOLD:
    #     raise NotEnoughValues(MISSING_TOO_MANY_FIELDS)
    return result


def simulation_data_from_file(file: FileStorage) -> List[SimulationData]:
    f = pandas.read_csv(file.stream, skiprows=1, encoding="utf-8")
    ret: List[SimulationData] = []
    for row_tuple in f.iterrows():
        row = row_tuple[1]
        millis = str(int(row.get(3)) * 1000) if int(row.get(3)) != 0 else "000000"
        try:
            timestamp = int(round(float(datetime.strptime("{} {} {}".format(row.get(1), row.get(2), millis),
                                                          "%d/%m/%Y %H:%M:%S %f").timestamp() * 1000)))
        except:
            timestamp = int(round(float(datetime.strptime("{} {} {}".format(row.get(1), row.get(2), millis),
                                                          "%Y-%m-%d %H:%M:%S %f").timestamp() * 1000)))
        set_point = float(row.get(4))
        process_value = float(row.get(5))
        out_value = float(row.get(6))
        ret.append(SimulationData(timestamp, process_value, set_point, out_value))
    return normalize_down(ret)


class RecommendationRequest:
    def __init__(self,
                 set_point_goal,
                 pid: PID,
                 convergence_time: Number,
                 simulation_data: List[SimulationData]):
        last_simulation_data = simulation_data[(len(simulation_data) - 1)]
        self.set_point = last_simulation_data.set_point if set_point_goal == "" else set_point_goal
        self.pid = pid
        self.convergence_time = convergence_time
        self.simulation_data = simulation_data
        self.current_sensor_value = last_simulation_data.process_value

    def __eq__(self, other):
        return self.pid == other.pid and self.set_point == other.set_point and \
               self.convergence_time == other.convergence_time and self.simulation_data == other.simulation_data and \
               self.current_sensor_value == other.current_sensor_value


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